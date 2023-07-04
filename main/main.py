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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ptext = "Salam, man behet komak mikonam tagvime darsito besazi"
    # ptext.encode(encoding='utf-8')

    # menutext = "Sakht"
    # menutext.encode(encoding='utf-8')

    keyboard = [
        ["Dars jadid ezafe kon"],
    ]

    if context.user_data['subs']:
        del context.user_data['subs']

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Salam, man behet komak mikonam tagvime darsito besazi",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True
            )
        )
    
    return OPTIONS

async def options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id
    if text == "Dars jadid ezafe kon":
        await context.bot.send_message(chat_id=chat_id, text="Esme dars:")
        return SUB
    
    elif text == "Reset":
        pass
    
    elif text == "Virayeshe dars":
        pass
    
    elif text == "Pak kardane dars":
        pass

    elif text == "Sakhte taghvim":
        pass

    else:
        pass

def main() -> None:
    app = Application.builder().token(TOKEN).build()

    convo_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            OPTIONS : [
                MessageHandler(
                    filters.Regex("^(Dars jadid ezafe kon|Reset|Virayeshe dars|Pak kardane dars|Sakhte taghvim)$"), options
                )
            ],
        },
    )

    app.add_handler(convo_handler)

    print('Polling...')

    # Run the bot
    app.run_polling()

# Run the program

if __name__ == '__main__':
    main()

    

