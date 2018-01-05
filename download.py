#!/usr/bin/env/python
import requests
import sqlite3
import vk
from urllib.parse import urlparse


VK_ACCESS_TOKEN = ''
VK_USER_ID = 1661695


def main(cursor, vk_api):
    offset = 0
    while offset < 27:
        print('+++++++++++++++++++++++++++++ {}'.format(offset))
        wall = vk_api.wall.get(owner_id=VK_USER_ID, offset=offset*100, count=100)
        wall.pop(0)
        for record in wall:
            # print(record)
            print('{} =>>> '.format(record['id']), end='')
            cursor.execute("select count(*) from gif where id = {}".format(record['id']))
            count = int(cursor.fetchone()[0])
            if count == 1:
                if record['post_type'] == 'copy' and 'attachment' in record and record['attachment']['type'] == 'doc' and \
                   record['attachment']['doc']['ext'] == 'gif':
                    try:
                        comment = record['text'].split('<br>')[0]
                        cursor.execute("delete from gif where id = {}".format(record['id']))
                        cursor.execute("insert into gif(id, link, comment) values({}, '{}', '{}')".format(record['id'], record['attachment']['doc']['url'], comment))
                        cursor.execute("commit;")
                        print('add')
                    except:
                        print(record)
                else:
                    print('not gif')
            else:
                print('skip')
        offset += 1


if __name__ == '__main__':
    session = vk.Session(access_token=VK_ACCESS_TOKEN)
    vk_api = vk.API(session)

    connection = sqlite3.connect('gifs.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE if not exists gif(
        id integer primary key,
        link text not null,
        comment text,
        used date)''')
    try:
        main(cursor, vk_api)
    finally:
        connection.close()