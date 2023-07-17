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

# TODO: check del and replace them with .clear() if needed
# TODO: set all the checks for presence of 'edit' and 'subs' to consider their length only, for example: if len(user_info.['subs] > 0)

from typing import Final
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, CallbackQuery
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

OPTIONS, SUB, DAY, STARTTIME, ENDTIME, TEACHER, CLASSNO, EDITSUB, EDITSUBCOL, DELETESUB = range(10)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ptext = "Salam, man behet komak mikonam tagvime darsito besazi"
    # ptext.encode(encoding='utf-8')

    # menutext = "Sakht"
    # menutext.encode(encoding='utf-8')

    keyboard = [
        ["Dars jadid ezafe kon"],
    ]

    context.user_data.clear()

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

    if 'subs' in context.user_data:
        user_data = context.user_data['subs']

    if text == "Dars jadid ezafe kon":
        if 'subs' not in context.user_data:
            context.user_data['subs'] = list()
        await context.bot.send_message(chat_id=chat_id, text="Esme dars:")
        return SUB
    
    elif text == "Reset":
        if context.user_data['subs']:
            context.user_data['subs'].clear()
            keyboard = [
                ["Dars jadid ezafe kon"],
            ]
            await context.bot.send_message(
                chat_id=chat_id,
                text="Baraye ezafe kardane darse jadid bezan roo dokme",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=keyboard,
                    one_time_keyboard=True
                    )
                )
            return OPTIONS

    elif text == "Virayeshe dars":
        keyboard = list()
        for row in context.user_data['subs']:
            keyboard.append([
                # InlineKeyboardButton(
                #     text=f"{row['id']}. Kelase {row['sub_title']}, {row['day']} ha az saate {row['start_time']} ta {row['end_time']}, ostad {row['teacher']}, kelase {row['classno']}",
                #     callback_data=f"{row['id']}"
                #     )]
                # )
                InlineKeyboardButton(
                    text=view([row]),
                    callback_data=f"{row['id']}"
                    )]
                )

        keyboard.append(
            [InlineKeyboardButton(
            text=f"Done✔✅",
            callback_data='done')]
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text="Koodoom dars ro mikhay virayesh koni?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return EDITSUB

    elif text == "Pak kardane dars":
        keyboard = list()
        for row in context.user_data['subs']:
            # keyboard.append([
            #     InlineKeyboardButton(
            #     text= f"{row['id']}. Kelase {row['sub_title']}, {row['day']} ha az saate {row['start_time']} ta {row['end_time']}, ostad {row['teacher']}, kelase {row['classno']}\n",
            #     callback_data=row['id'])
            #     ])

            keyboard.append([
                InlineKeyboardButton(
                    text=view([row]),
                    callback_data=f"{row['id']}"
                    )]
                )

        keyboard.append(
            [InlineKeyboardButton(
            text=f"Done✔✅",
            callback_data='done')]
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text="Koodoom dars ro mikhay pak koni?",
            reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        return DELETESUB

    elif text == "Sakhte taghvim":
        pass

    else:
        keyboard = [
            ["Dars jadid ezafe kon"],
        ]
        
        if len(context.user_data['subs']) > 0:
            keyboard.append(
                ["Reset"],
                ["Virayeshe dars"],
                ["Pak kardane dars"],
                ["Sakhte taghvim"]
            )

        await context.bot.send_message(
            chat_id=chat_id,
            text="Command e eshtebah. Dobare entekhab kon:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard,
                one_time_keyboard=True)
            )
        
        return OPTIONS


async def sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    text = str(update.message.text)
    chat_id = update.message.chat_id
    if 'edit' in user_data:
        for row in user_data['subs']:
            if row['id'] == user_data['edit']['id']:
                keyboard = list()
                row['sub_title'] = text
                sub_data  = list(user_data['subs'][int(user_data['edit']['id'])-1].items())

                for i in range(1, len(sub_data)):
                    keyboard.append([
                        InlineKeyboardButton(
                        text=f"{sub_data[i][0]}:{sub_data[i][1]}",
                        callback_data=sub_data[i][0])
                        ])
                
                keyboard.append(
                    [InlineKeyboardButton(
                    text=f"Done✔✅",
                    callback_data='done')]
                )
                
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Kodoom ghesmat ro mikhay virayesh koni:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                return EDITSUBCOL
    else:
        if len(context.user_data['subs']) > 0:
            sub_id = int(context.user_data['subs'][-1]['id'])
            context.user_data['subs'].append(
                    {
                    'id' : str(sub_id+1),
                    'sub_title' : text
                    }
                )
        else:
            context.user_data['subs'] = [
                    {
                    'id' : '1',
                    'sub_title' : text
                    }
                ]

        keyboard = [
            [InlineKeyboardButton('Shanbe', callback_data='Shanbe')],
            [InlineKeyboardButton('Yekshanbe', callback_data='Yekshanbe')],
            [InlineKeyboardButton('Doshanbe', callback_data='Doshanbe')],
            [InlineKeyboardButton('Seshanbe', callback_data='Seshanbe')],
            [InlineKeyboardButton('Chaarshanbe', callback_data='Chaarshanbe')],
            [InlineKeyboardButton('Panjshanbe', callback_data='Panjshanbe')],
            [InlineKeyboardButton('Jome', callback_data='Jome')],
        ]

        await context.bot.send_message(
            chat_id=chat_id,
            text="Rooz:",
            reply_markup=InlineKeyboardMarkup(keyboard)
            )
        return DAY

async def day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_data = context.user_data
    await query.answer(
        text="Button clicked"
    )

    if 'edit' in user_data:
        for row in user_data['subs']:
            if row['id'] == user_data['edit']['id']:
                keyboard = list()
                row['day'] = query.data
                sub_data  = list(user_data['subs'][int(user_data['edit']['id'])-1].items())

                for i in range(1, len(sub_data)):
                    keyboard.append([
                        InlineKeyboardButton(
                        text=f"{sub_data[i][0]}:{sub_data[i][1]}",
                        callback_data=sub_data[i][0])
                        ])

                keyboard.append(
                    [InlineKeyboardButton(
                    text=f"Done✔✅",
                    callback_data='done')]
                )    
                
                await query.edit_message_text(
                    text="Kodoom ghesmat ro mikhay virayesh koni:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                
                return EDITSUBCOL
    else:
        context.user_data['subs'][-1]['day'] = query.data
        await query.edit_message_text(text="Saate shorooe kelas: (Masalan 14:40)")
        return STARTTIME

async def starttime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.split(':')

    # in case user didn't submit minutes for a class that starts at 
    if len(text) == 1 :
        text.append('00')

    chat_id = update.message.chat_id
    user_data = context.user_data

    try:
        if 0 <= int(text[0]) < 24:
            if 0 <= int(text[0]) < 60:
                if 'edit' in user_data:
                    for row in user_data['subs']:
                        if row['id'] == user_data['edit']['id']:
                            keyboard = list()
                            row['start_time'] = text
                            sub_data  = list(user_data['subs'][int(user_data['edit']['id'])-1].items())

                            for i in range(1, len(sub_data)):
                                keyboard.append([
                                    InlineKeyboardButton(
                                    text=f"{sub_data[i][0]}:{sub_data[i][1]}",
                                    callback_data=sub_data[i][0])
                                    ])

                            keyboard.append(
                                [InlineKeyboardButton(
                                text=f"Done✔✅",
                                callback_data='done')]
                            )    
                            
                            await context.bot.send_message(
                                chat_id=chat_id,
                                text="Kodoom ghesmat ro mikhay virayesh koni:",
                                reply_markup=InlineKeyboardMarkup(keyboard)
                                )
                            return EDITSUBCOL
                else:
                    context.user_data['subs'][-1]['start_time'] = time(hour=int(text[0]),minute=int(text[1]))
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="Saate payane kelas: (Masalan 17:35)"
                        )
                    return ENDTIME
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Daghighe shorooe kelas eshtebahe, dobare saate shooroo ro vared kon: (Masalan 14:40)"
                    )
                return STARTTIME
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Saate shorooe kelas eshtebahe, dobare vared kon: (Masalan 14:40)"
                )
            return STARTTIME
    except ValueError:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Eshtebah vared kardi dobare vared kon: (Masalan 14:40)"
            )
        return STARTTIME

async def endtime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.split(':')

    # in case user didn't submit minutes for a class that ends at 
    if len(text) == 1 :
        text.append('00')

    chat_id = update.message.chat_id
    user_data = context.user_data
    try:
        if 0 <= int(text[0]) < 24:
            if 0 <= int(text[0]) < 60:
                if 'edit' in user_data:
                    for row in user_data['subs']:
                        if row['id'] == user_data['edit']['id']:
                            keyboard = list()
                            row['end_time'] = text
                            sub_data  = list(user_data['subs'][int(user_data['edit']['id'])-1].items())
                            for i in range(1, len(sub_data)):
                                keyboard.append([
                                    InlineKeyboardButton(
                                    text=f"{sub_data[i][0]}:{sub_data[i][1]}",
                                    callback_data=sub_data[i][0])
                                    ])
                            
                            keyboard.append(
                                [InlineKeyboardButton(
                                text=f"Done✔✅",
                                callback_data='done')]
                            )

                            await context.bot.send_message(
                                chat_id=chat_id,
                                text="Kodoom ghesmat ro mikhay virayesh koni:",
                                reply_markup=InlineKeyboardMarkup(keyboard)
                                )
                            return EDITSUBCOL
                else:
                    context.user_data['subs'][-1]['end_time'] = time(hour=int(text[0]),minute=int(text[1]))
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="Esme ostad:"
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
    text = str(update.message.text)
    chat_id = update.message.chat_id
    user_data = context.user_data
    if 'edit' in user_data:
        for row in user_data['subs']:
            if row['id'] == user_data['edit']['id']:
                keyboard = list()
                row['teacher'] = text
                sub_data  = list(user_data['subs'][int(user_data['edit']['id'])-1].items())
                for i in range(1, len(sub_data)):
                    keyboard.append([
                        InlineKeyboardButton(
                        text=f"{sub_data[i][0]}:{sub_data[i][1]}",
                        callback_data=sub_data[i][0])
                        ])
                
                keyboard.append(
                    [InlineKeyboardButton(
                    text=f"Done✔✅",
                    callback_data='done')]
                )

                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Kodoom ghesmat ro mikhay virayesh koni:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                return EDITSUBCOL
    else:
        context.user_data['subs'][-1]['teacher'] = text
        await context.bot.send_message(
            chat_id=chat_id,
            text="Shomare kelas:"
            )
        return CLASSNO

async def classno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = str(update.message.text)
    chat_id = update.message.chat_id
    user_data = context.user_data
    if 'edit' in user_data:
        for row in user_data['subs']:
            if row['id'] == user_data['edit']['id']:
                keyboard = list()
                row['classno'] = text
                sub_data  = list(user_data['subs'][int(user_data['edit']['id'])-1].items())
                for i in range(1, len(sub_data)):
                    keyboard.append([
                        InlineKeyboardButton(
                        text=f"{sub_data[i][0]}:{sub_data[i][1]}",
                        callback_data=sub_data[i][0])
                        ])
                    
                keyboard.append(
                    [InlineKeyboardButton(
                    text=f"Done✔✅",
                    callback_data='done')]
                )

                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Kodoom ghesmat ro mikhay virayesh koni:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                return EDITSUBCOL
    else:
        context.user_data['subs'][-1]['classno'] = text
        data = context.user_data['subs']
        keyboard = [
            ["Dars jadid ezafe kon"],
            ["Reset"],
            ["Virayeshe dars"],
            ["Pak kardane dars"],
            ["Sakhte taghvim"]
        ]
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Etelaat vared shod. Ina dars haeie ke ta alan vared kardi:\n{view(data=data)}",
            reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            one_time_keyboard=True
            )
        )
        return OPTIONS

async def editsub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_data = context.user_data

    await query.answer(text="Button clicked")
    if query.data == 'done':
        if 'edit' in context.user_data:
            del context.user_data['edit']

        keyboard = [
            ["Dars jadid ezafe kon"],
            ["Reset"],
            ["Virayeshe dars"],
            ["Pak kardane dars"],
            ["Sakhte taghvim"]
        ]

        await query.message.reply_text(
            text=f"Ina dars haeie ke ta alan vared kardi:\n{view(data=context.user_data['subs'])}",
            reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            one_time_keyboard=True
            )
        )
        return OPTIONS
    else:
        if int(query.data) <= int(user_data['subs'][-1]['id']):
            user_data['edit'] = {'id' : str(query.data)}
            keyboard = list()
            sub_data  = list(user_data['subs'][int(query.data)-1].items())
            for i in range(1, len(sub_data)):
                keyboard.append([
                    InlineKeyboardButton(
                    text=f"{sub_data[i][0]}:{sub_data[i][1]}",
                    callback_data=sub_data[i][0])
                    ])
                
            keyboard.append(
                [InlineKeyboardButton(
                text=f"Done✔✅",
                callback_data='done')]
            )
            await query.edit_message_text(
                text="Kodoom ghesmat ro mikhay virayesh koni:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return EDITSUBCOL
        else:
            keyboard = list()
            for row in user_data['subs']:
                keyboard.append([
                    InlineKeyboardButton(
                        text=view([row]),
                        callback_data=f"{row['id']}"
                        )]
                    )

            keyboard.append(
                [InlineKeyboardButton(
                text=f"Done✔✅",
                callback_data='done')]
            )
            await query.edit_message_text(
                text="Dars yaft nashod dobare entekhab kon:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return EDITSUB


async def editsubcol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(text="Button clicked.")

    if query.data == 'sub_title':
        await query.edit_message_text(
            text="Esme jadide dars:"
        )
        return SUB

    elif query.data == 'day':
        keyboard = [
            [InlineKeyboardButton('Shanbe', callback_data='Shanbe')],
            [InlineKeyboardButton('Yekshanbe', callback_data='Yekshanbe')],
            [InlineKeyboardButton('Doshanbe', callback_data='Doshanbe')],
            [InlineKeyboardButton('Seshanbe', callback_data='Seshanbe')],
            [InlineKeyboardButton('Chaarshanbe', callback_data='Chaarshanbe')],
            [InlineKeyboardButton('Panjshanbe', callback_data='Panjshanbe')],
            [InlineKeyboardButton('Jome', callback_data='Jome')],
        ]

        await query.edit_message_text(
            text="Rooze jadide dars:",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )
        return DAY
    
    elif query.data == 'start_time':
        await query.edit_message_text(
            text="Saate shoorooe jadid:",
        )
        return STARTTIME
    
    elif query.data == 'end_time':
        await query.edit_message_text(
            text="Saate payane jadid:",
        )
        return ENDTIME
    
    elif query.data == 'teacher':
        await query.edit_message_text(
            text="Esme jadide ostad:",
        )
        return TEACHER
    
    elif query.data == 'classno':
        await query.edit_message_text(
            text="Shomare jadide kelas:",
        )
        return CLASSNO
    
    elif query.data == 'done':
        keyboard = list()
        for row in context.user_data['subs']:
            # keyboard.append([
            #     InlineKeyboardButton(
            #         text=f"{row['id']}. Kelase {row['sub_title']}, {row['day']} ha az saate {row['start_time']} ta {row['end_time']}, ostad {row['teacher']}, kelase {row['classno']}",
            #         callback_data=f"{row['id']}"
            #         )]
            #     )
            keyboard.append([
                InlineKeyboardButton(
                    text=view([row]),
                    callback_data=f"{row['id']}"
                    )]
                )

        keyboard.append(
            [InlineKeyboardButton(
            text=f"Done✔✅",
            callback_data='done')]

        )

        await query.edit_message_text(
            text="Koodoom dars ro mikhay virayesh koni?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return EDITSUB
    
    else:
        # TODO currently the following code is copy-pasted. Find a way to create a manual update to re-use the editsub function        
        user_data = context.user_data
        sub_data  = list(user_data['subs'][int(query.data)-1].items())
        for i in range(1, len(sub_data)):
            keyboard.append([
                InlineKeyboardButton(
                text=f"{sub_data[i][0]}:{sub_data[i][1]}",
                callback_data=sub_data[i][0])
                ])
        await query.edit_message_text(
            text="Commande eshtebah\nKodoom ghesmat ro mikhay virayesh koni:",
            reply_markup=InlineKeyboardMarkup(keyboard)
            )
        return EDITSUBCOL

async def deletesub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    i = subtract = 0
    subs = context.user_data['subs']
    await query.answer("Button selected.")

    try:
        if int(query.data) <= int(subs[-1]['id']):
            while i < len(subs):
                subs[i]['id'] = str(int(subs[i]['id']) - subtract)

                if (subs[i]['id'] == str(query.data)) and (subtract == 0):
                    del subs[i]
                    subtract = 1
                    continue

                i += 1
        
            keyboard = list()
            for row in context.user_data['subs']:

                keyboard.append([
                    InlineKeyboardButton(
                        text=view([row]),
                        callback_data=f"{row['id']}"
                        )]
                    )

            keyboard.append(
                [InlineKeyboardButton(
                text=f"Done✔✅",
                callback_data='done')]
            )

            await query.edit_message_text(
                text="Dars pak shod.\nKoodoom darse dige ro mikhay pak koni?",
                reply_markup=InlineKeyboardMarkup(keyboard)
                )
            
            return DELETESUB
        else:

            keyboard = list()
            for row in context.user_data['subs']:

                keyboard.append([
                    InlineKeyboardButton(
                        text=view([row]),
                        callback_data=f"{row['id']}"
                        )]
                    )

            keyboard.append(
                [InlineKeyboardButton(
                text=f"Done✔✅",
                callback_data='done')]
            )

            await query.edit_message_text(
                text="Dars yaft nashod.\nKoodoom darse dige ro mikhay pak koni?",
                reply_markup=InlineKeyboardMarkup(keyboard)
                )
            
            return DELETESUB


    except ValueError:
        if query.data == 'done':
            keyboard = [
                ["Dars jadid ezafe kon"],
                ["Reset"],
                ["Virayeshe dars"],
                ["Pak kardane dars"],
                ["Sakhte taghvim"]
            ]

            await query.message.reply_text(
            text="Dars paak shod.\nGozine morede nazar ro entekhab kon",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard,
                one_time_keyboard=True)
            )
    
            return OPTIONS

        else:
    
            keyboard = list()
            for row in context.user_data['subs']:

                keyboard.append([
                    InlineKeyboardButton(
                        text=view([row]),
                        callback_data=f"{row['id']}"
                        )]
                    )

            keyboard.append(
                [InlineKeyboardButton(
                text=f"Done✔✅",
                callback_data='done')]
            )

            await query.edit_message_text(
                text="Dars yaft nashod. Koodoom dars ro mikhay pak koni?",
                reply_markup=InlineKeyboardMarkup(keyboard)
                )
            
            return DELETESUB
    

def view(data: list):
    text = ''
    print("data: \n", data)
    for row in data:
        print("row: \n", row)
        text += "{id}. Kelase {sub_title}, {day} ha az saate {start_time} ta {end_time}, ostad {teacher}, kelase {classno}\n".format(id = row['id'], sub_title = row['sub_title'], day = row['day'], start_time = str(row['start_time'].strftime("%H:%M")), end_time = str(row['end_time'].strftime("%H:%M")), teacher = row['teacher'], classno = row['classno'])
        # text += "{sub_id}. Kelase ".format(sub_id = row['id'])
        # text += "{sub_title}, ".format(sub_title = row['sub_title'])
        # text += "{day} ha az saate".format(day = row['day'])
        # text += "{start_time} ta".format(start_time = str(row['start_time'].strftime("%H:%M")))
        # text += "{end_time}, ostad ".format(end_time = str(row['end_time'].strftime("%H:%M")))
        # text += "{teacher}, kelase ".format(teacher = row['teacher'])
        # text += "{classno}\n".format(classno = row['classno'])
    return text



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
            EDITSUB : [
                CallbackQueryHandler(editsub, pattern="^([1-9][0-9]*|done)$")
            ],
            EDITSUBCOL : [
                CallbackQueryHandler(editsubcol, pattern="^(sub_title|day|start_time|end_time|teacher|classno|done)$")
            ],
            DELETESUB : [
                CallbackQueryHandler(deletesub, pattern="^([1-9][0-9]*|done)$")
            ],
        },
        fallbacks=[CommandHandler('sub', sub)],
        per_chat=True,
        per_user=True
    )

    app.add_handler(convo_handler)

    print('Polling...')

    # Run the bot
    app.run_polling()

# Run the program

if __name__ == '__main__':
    main()