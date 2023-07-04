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

async def sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if 'subs' in context.user_data:
        sub_id = context.user_data['subs'][-1]['id']
        context.user_data['subs'].append({'id' : sub_id+1, 'sub_title' : text})
    else:
        context.user_data['subs'] = [{'id' : 1, 'sub_title' : text}]

    keyboard = [
        [InlineKeyboardButton('Shanbe', callback_data='Shanbe')],
        [InlineKeyboardButton('Yekshanbe', callback_data='Yekshanbe')],
        [InlineKeyboardButton('Doshanbe', callback_data='Doshanbe')],
        [InlineKeyboardButton('Seshanbe', callback_data='Seshanbe')],
        [InlineKeyboardButton('Chaarshanbe', callback_data='Chaarshanbe')],
        [InlineKeyboardButton('Panjshanbe', callback_data='Panjshanbe')],
        [InlineKeyboardButton('Jome', callback_data='Jome')],
    ]

    await context.bot.send_message(chat_id=update.message.chat_id, text="Rooz:", reply_markup=InlineKeyboardMarkup(keyboard))
    # print(context.user_data['subs'])
    return DAY

async def day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id
    query = update.callback_query
    await query.answer()
    context.user_data['subs'][-1]['day'] = query.data
    await query.edit_message_text(text="Saate shorooe kelas: (Masalan 14:40)")
    return STARTTIME

async def starttime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.split(':')
    chat_id = update.message.chat_id
    try:
        if 0 <= int(text[0]) < 24:
            if 0 <= int(text[0]) < 60:
                context.user_data['subs'][-1]['starttime'] = time(hour=text[0],minute=text[1])
                await context.bot.send_message(chat_id=chat_id, text="Saate payane kelas: (Masalan 17:35)")
                return ENDTIME
            else:
                await context.bot.send_message(chat_id=chat_id, text="Daghighe shorooe kelas eshtebahe, dobare saate shooroo ro vared kon: (Masalan 14:40)")
                return STARTTIME
        else:
            await context.bot.send_message(chat_id=chat_id, text="Saate shorooe kelas eshtebahe, dobare vared kon: (Masalan 14:40)")
            return STARTTIME
    except ValueError:
        await context.bot.send_message(chat_id=chat_id, text="Eshtebah vared kardi dobare vared kon: (Masalan 14:40)")
        return STARTTIME

async def endtime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.split(':')
    chat_id = update.message.chat_id
    try:
        if 0 <= int(text[0]) < 24:
            if 0 <= int(text[0]) < 60:
                context.user_data['subs'][-1]['endtime'] = time(hour=text[0],minute=text[1])
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Saate payane kelas: (Masalan 17:35)"
                    )
                return TEACHER
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Daghighe payane kelas eshtebahe, dobare saate shooroo ro vared kon: (Masalan 14:40)"
                    )
                return ENDTIME
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Saate payane kelas eshtebahe, dobare vared kon: (Masalan 14:40)"
                )
            return ENDTIME
    except ValueError:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Eshtebah vared kardi, dobare vared kon: (Masalan 14:40)"
            )
        return ENDTIME

async def teacher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id
    context.user_data['subs'][-1]['teacher'] = text
    await context.bot.send_message(
        chat_id=chat_id,
        text="Shomare kelas:"
        )
    return CLASSNO

async def classno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id
    context.user_data['subs'][-1]['classno'] = text
    keyboard = []
    data = context.user_data['subs']
    # for row in data:
    #     keyboard.append(
    #             [InlineKeyboardButton(
    #                 text=f"{row['id']}. Kelase {row['sub']}, {row['day']} ha az saate{row['starttime']} ta {row['endtime']}, ostad {row['teacher']}, kelase {row['classno']}",
    #                 callback_data=f"{row['id']}"
    #             )]
    #         )
    keyboard = [
        ["Reset"],
        ["Virayeshe dars"],
        ["Pak kardane dars"],
        ["Sakhte taghvim"]
    ]
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"Etelaat vared shod. Ina dars haeie ke ta alan vared kardi:\n{view(data=data)}",
        reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True)
    )
    return OPTIONS

def view(data):
    text = ''
    for row in data:
       text += f"{row['id']}. Kelase {row['sub']}, {row['day']} ha az saate{row['starttime']} ta {row['endtime']}, ostad {row['teacher']}, kelase {row['classno']}\n",


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
            SUB : [
                MessageHandler(
                    (filters.TEXT & ~filters.COMMAND) , sub
                )
            ],
            DAY : [
                CallbackQueryHandler(day, pattern="^(Shanbe|Yekshanbe|Doshanbe|Seshanbe|Chaarshanbe|Panjshanbe|Jome)$")
            ],
            STARTTIME : [
                MessageHandler(
                    (filters.TEXT & ~filters.COMMAND), starttime
                )
            ],
            ENDTIME : [
                MessageHandler(
                    (filters.TEXT & ~filters.COMMAND), endtime
                )
            ],
            TEACHER : [
                MessageHandler(
                    (filters.TEXT & ~filters.COMMAND), teacher
                )
            ],
            CLASSNO : [
                MessageHandler(
                    (filters.TEXT & ~filters.COMMAND), classno
                )
            ],
        },
        fallbacks=[CommandHandler('sub', sub)]
    )

    app.add_handler(convo_handler)

    print('Polling...')

    # Run the bot
    app.run_polling()

# Run the program

if __name__ == '__main__':
    main()

    

