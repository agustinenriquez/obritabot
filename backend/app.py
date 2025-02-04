from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace with your own token
TELEGRAM_TOKEN = '7658861058:AAE13jvC_LigFZ1VuasbG7X9T-H5BMy8aw4'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am your bot.')

def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
