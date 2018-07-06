# -*- coding: utf-8 -*-
import sqlite3
from contextlib import closing

dbname = 'user.db'

try:
    # followされた時
    def event_follow(time,id):
        with closing(sqlite3.connect(dbname)) as conn:
            c = conn.cursor()

            # データベースがなければ作成
            create_table = '''create table if not exists users (no integer PRIMARY KEY AUTOINCREMENT, id varchar(64),
                              date varchar(20))'''
            c.execute(create_table)

            # データベース登録
            sql = 'insert into users (no, id, date) values (?,?,?)'
            user = (None, id, time)
            c.execute(sql, user)

            conn.commit()

            select_sql = 'select * from users'
            for row in c.execute(select_sql):
                print(row)
except:
    None

try:
    # unfollowされた時
    def event_unfollow(id):
        with closing(sqlite3.connect(dbname)) as conn:
            c = conn.cursor()

            sql = 'delete from users where id = ?'
            delete_id = id
            c.execute(sql, (delete_id,))

            conn.commit()
except:
    None

try:
    # pushメッセージを送信する時
    def get_user():
        with closing(sqlite3.connect(dbname)) as conn:
            c = conn.cursor()
            user = []

            select_sql = 'select id from users'

            for row in c.execute(select_sql):
                user.append(row[0])
            # 登録されているユーザーのuserIdを返す
            return user
    # app.pyのsend_message()を実行してPUSHメッセージを飛ばす
    app.send_message()

except:
    None
