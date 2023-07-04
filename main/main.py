# from pathlib import Path
# import calendar

# def Print(text):
#     output_file=open('main/output.txt', mode='w', encoding='utf-8')
#     for line in text:
#         output_file.write(line)
#     output_file.close()

# file_path = 'main/test.txt'

# file = open(file_path, mode='r', encoding='utf-8')

# rows = file.readlines()
# row = rows[1]
# row = row.split("")
# Print(row)

# file.close()

from typing import Final
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters, ContextTypes

from urllib.parse import quote

from datetime import time

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


print('Starting up bot...')

# TOKEN = '6255015100:AAGzUSK9WaUVeBFl4E-y-gUq6c18cqToUi4'
TOKEN: Final = '6255015100:AAGzUSK9WaUVeBFl4E-y-gUq6c18cqToUi4'
BOT_USERNAME: Final = '@Ghasem123456789bot'

OPTIONS, SUB, DAY, STARTTIME, ENDTIME, TEACHER, CLASSNO = range(7)

def main() -> None:
    app = Application.builder().token(TOKEN).build()


    print('Polling...')

    # Run the bot
    app.run_polling()

# Run the program

if __name__ == '__main__':
    main()

    

