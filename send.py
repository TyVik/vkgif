#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import choice
from urllib.parse import quote
import sqlite3

from telegram.bot import Bot


CHAT_ID = ''
BOT_KEY = ''

def main(cursor, bot):
    def get_id(cursor):
        cursor.execute('select id from gif where used is null;')
        row = choice(cursor.fetchall())
        result = row[0]
        cursor.execute("update gif set used = DATETIME('now') where id = {}".format(result))
        return result

    try:
        id = get_id(cursor)
        cursor.execute('select * from gif where id = {}'.format(id))
        row = cursor.fetchone()
        bot.sendVideo(CHAT_ID, video=row[1], caption=row[3])
    except Exception as e:
        main(cursor, bot)

def clear(cursor):
    cursor.execute('update gif set used = null')

if __name__ == '__main__':
    bot = Bot(BOT_KEY)
    db = sqlite3.connect('gif.db')
    cursor = db.cursor()
    try:
        clear(cursor)
        main(cursor, bot)
    finally:
        db.close()