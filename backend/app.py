from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from datetime import datetime, timedelta
from cac_scraper import scrape_cac_index_alternative, get_cached_cac_value, cache_cac_value, update_last_run_timestamp, should_run_test

# Replace with your own token
TELEGRAM_TOKEN = '7658861058:AAE13jvC_LigFZ1VuasbG7X9T-H5BMy8aw4'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text('Hello! I am your bot.')

async def cac(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        if not should_run_test():
            cached_value = get_cached_cac_value()
            if cached_value:
                await update.message.reply_text(f"Using cached CAC Index: {cached_value}")
                return
            else:
                await update.message.reply_text("Test already run within the last 24 hours, but no cached value found. Scraping new value.")
        
        cac_index_alternative = scrape_cac_index_alternative()
        if cac_index_alternative:
            await update.message.reply_text(f"CAC Index from ikiwi: {cac_index_alternative}")
            update_last_run_timestamp()
            cache_cac_value(cac_index_alternative)
        else:
            await update.message.reply_text("Failed to scrape CAC Index from ikiwi")

async def cuartos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        try:
            # Extract the number of rooms from the command argument
            rooms = int(context.args[0])
            await update.message.reply_text(f"Number of rooms: {rooms}")
        except (IndexError, ValueError):
            await update.message.reply_text("Please provide a valid number of rooms. Usage: /cuartos <number>")

def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start))
    # Register the /cac command handler
    application.add_handler(CommandHandler("cac", cac))
    # Register the /cuartos command handler
    application.add_handler(CommandHandler("cuartos", cuartos))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()