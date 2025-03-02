import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
import os

from backend.scrape_news import scrape_news

class TestScrapeNews(unittest.TestCase):

    @patch('backend.scrape_news.requests.get')
    @patch('backend.scrape_news.open', new_callable=mock_open)
    @patch('backend.scrape_news.os.path.exists')
    def test_scrape_news(self, mock_exists, mock_open, mock_get):
        # Mock the response from requests.get
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = '''
        <div class="article-content">
            <h2>Test Title</h2>
            <p>Test Summary</p>
        </div>
        '''
        
        # Mock the flag file behavior
        mock_exists.return_value = False
        
        # Call the function
        scrape_news()
        
        # Check if the news was printed
        mock_open.assert_called_with('/home/m0tz/obritabot/backend/scrape_flag.txt', 'w')
        handle = mock_open()
        handle.write.assert_called_with(datetime.now().strftime('%Y-%m-%d'))

    @patch('backend.scrape_news.os.path.exists')
    @patch('backend.scrape_news.open', new_callable=mock_open, read_data=datetime.now().strftime('%Y-%m-%d'))
    def test_scrape_news_already_scraped(self, mock_open, mock_exists):
        # Mock the flag file behavior
        mock_exists.return_value = True
        
        # Call the function
        with patch('builtins.print') as mocked_print:
            scrape_news()
            mocked_print.assert_called_with("News already scraped today. Skipping...")

if __name__ == '__main__':
    unittest.main()
