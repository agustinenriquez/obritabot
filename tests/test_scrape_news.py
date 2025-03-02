import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os

# Add the backend directory to the sys.path to import scrape_news
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
import scrape_news

class TestScrapeNews(unittest.TestCase):

    @patch('scrape_news.requests.get')
    @patch('scrape_news.save_news_to_db')
    @patch('scrape_news.get_news_from_db')
    @patch('scrape_news.open', new_callable=MagicMock)
    @patch('scrape_news.os.path.exists')
    def test_scrape_news(self, mock_exists, mock_open, mock_get_news_from_db, mock_save_news_to_db, mock_requests_get):
        # Mock the database to return None (no cached news)
        mock_get_news_from_db.return_value = None

        # Mock the requests.get to return a fake response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '''
        <div class="article-content">
            <h2>Test Title 1</h2>
            <p>Test Summary 1</p>
        </div>
        <div class="article-content">
            <h2>Test Title 2</h2>
            <p>Test Summary 2</p>
        </div>
        '''
        mock_requests_get.return_value = mock_response

        # Mock the flag file behavior
        mock_exists.return_value = False

        # Call the scrape_news function
        scrape_news.scrape_news()

        # Check if save_news_to_db was called with the correct parameters
        today = datetime.now().strftime('%Y-%m-%d')
        expected_content = (
            "Title: Test Title 1\nSummary: Test Summary 1\n" + "-" * 40 + "\n" +
            "Title: Test Title 2\nSummary: Test Summary 2\n" + "-" * 40 + "\n"
        )
        mock_save_news_to_db.assert_called_once_with(today, expected_content)

        # Check if the flag file was created
        mock_open.assert_called_with('/home/m0tz/obritabot/backend/scrape_flag.txt', 'w')
        handle = mock_open()
        handle().write.assert_called_with(today)

    @patch('scrape_news.get_news_from_db')
    def test_scrape_news_cached(self, mock_get_news_from_db):
        # Mock the database to return cached news
        mock_get_news_from_db.return_value = "Cached news content"

        # Capture the output
        with patch('builtins.print') as mocked_print:
            scrape_news.scrape_news()
            mocked_print.assert_any_call("News already scraped today. Retrieving from cache...")
            mocked_print.assert_any_call("Cached news content")

    @patch('scrape_news.get_news_from_db')
    @patch('scrape_news.os.path.exists')
    @patch('scrape_news.open', new_callable=MagicMock)
    def test_scrape_news_already_scraped(self, mock_open, mock_exists, mock_get_news_from_db):
        # Mock the database to return None (no cached news)
        mock_get_news_from_db.return_value = None

        # Mock the flag file behavior
        mock_exists.return_value = True

        # Mock the flag file content
        mock_open.return_value.read.return_value = datetime.now().strftime('%Y-%m-%d')

        # Capture the output
        with patch('builtins.print') as mocked_print:
            scrape_news.scrape_news()
            mocked_print.assert_called_with("News already scraped today. Skipping...")

if __name__ == '__main__':
    print("Running tests...")
    unittest.main()
