# chatbot.py
import random
from random import randint
import pymysql
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

import configparser
import logging




def db_connect():
    db = pymysql.connect(host='cloudcomputing.c8zsz8bm7sbi.us-east-1.rds.amazonaws.com', user='admin', password='swQ50wDD9xXEuGZwDpva', database='chatbot')
    return db


def show_reviews():
    db = db_connect()
    cursor = db.cursor()
    sql = "SELECT * FROM review"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        return results
    except:
        print("Error: unable to fetch data")


def add_review(movie_name, movie_review):
    db = db_connect()
    cursor = db.cursor()
    sql = "INSERT INTO review(movie_name, movie_review) VALUES ('%s', '%s')" % (movie_name, movie_review)
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
    except:
        print("Error")


def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    # updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # # register a dispatcher to handle message: here we register an echo dispatcher
    menu_handler = MessageHandler(Filters.text & (~Filters.command), show_menu)
    dispatcher.add_handler(menu_handler)

    # # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("photo", photo))
    dispatcher.add_handler(CommandHandler("video", video))
    dispatcher.add_handler(CommandHandler("review", review))
    dispatcher.add_handler(CommandHandler('maths', maths))
    dispatcher.add_handler(CallbackQueryHandler(answer))
    # To start the bot:
    updater.start_polling()
    updater.idle()


def show_menu(update, context):
    update.message.reply_text('''Hello! Welcome to CC chatbot! 
Please select the following functions:

1. Type '/photo' to see hiking photos 
ex: /photo victoria, /photo changzhou
2. Type '/video' to see cooking videos 
ex: /video cooking
3. Type '/review' to read TV show reviews
ex: /review read''')


def photo(update: Update, context: CallbackContext) -> None:
    msg = context.args[0]
    if msg == 'victoria':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('img/t1-2.jpg', 'rb'))
    elif msg == 'changzhou':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('img/t2-2.jpg', 'rb'))
    else:
        update.message.reply_text("Sorry, I didn't have any photos related to " + msg + "!")


def video(update: Update, context: CallbackContext) -> None:
    msg = context.args[0]
    if msg == 'cooking':
        context.bot.send_video(chat_id=update.effective_chat.id, video=open('video/2.mp4', 'rb'))
    else:
        update.message.reply_text("Sorry, I didn't have any videos related to " + msg + "!")


def review(update: Update, context: CallbackContext) -> None:
    msg = context.args[0]
    # if msg == 'write':
    #     movie_name = context.args[1]
    #     movie_review = context.args[2]
    #     # add_review(movie_name, movie_review)
    #     print(movie_name, movie_review)
    if msg == 'read':
        results = show_reviews()
        for i in results:
            update.message.reply_text(i[1] + ': ' + i[2])
    else:
        update.message.reply_text("Please input the right command!")


if __name__ == '__main__':
    main()



def maths(update, context):
    a, b = randint(1, 100), randint(1, 100)
    update.message.reply_text('{} + {} = ?'.format(a, b),
        reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(str(s), callback_data = '{} {} {}'.format(a, b, s)) for s in range(a + b - randint(1, 3), a + b + randint(1, 3))
            ]]))

def answer(update, context):
    a, b, s = [int(x) for x in update.callback_query.data.split()]
    if a + b == s:
        update.callback_query.edit_message_text('Correct! You must smarter than Grade 1 students :)')
    else:
        update.callback_query.edit_message_text('Wrong! OMG, you are even worse than Grade 1 students :(')






if __name__ == '__main__':
    main()
