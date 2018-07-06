from flask import Flask, request, abort
import os
import urllib.request
import json
import calendar
import db
import send
from flask import jsonify
from datetime import *
from dateutil.relativedelta import *

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_SECRET', None))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None))

@app.route("/")
def hello_world():
    return "hello world!"

# json受け取り
@app.route('/webhook', methods=['POST','GET'])
def webhook():
    reply_to_line(request.json)
    return "OK"

def reply_to_line(body):
    resp = json.dumps(body,ensure_ascii=False)
    get_param(json.loads(resp))

# jsonデータ格納
def get_param(d):
    # messageを受け取った時
    if d['events'][0]['type'] == "message":
        token = d['events'][0]['source']['userId']
        text = d['events'][0]['message']['text']
        reply_token = d['events'][0]['replyToken']
        if text=="menu1":
            check_shift(token)
        elif text=="menu2":
            line_bot_api.reply_message(reply_token, TextSendMessage(text="hello"))
        else:
            None

    # followされた時
    elif d['events'][0]['type'] == "follow":
        time = d['events'][0]['timestamp']
        id = d['events'][0]['source']['userId']

        db.event_follow(time,id)

    # unfollowされた時
    elif d['events'][0]['type'] == "unfollow":
        id = d['events'][0]['source']['userId']

        db.event_unfollow(id)

# 次の金曜日を計算
def next_friday():
    now = datetime.now()
    today = date.today()
    next = today + relativedelta(weekday=FR(+1))
    start = today + relativedelta(weekday=SU(+2))
    finish = today + relativedelta(weekday=SA(+3))
    # 締切日(次の金曜日)
    closing_date = "{0:%Y年%m月%d日}".format(next)
    # 提出期間
    period = "{0:%m月%d日}".format(start)+"〜"+"{0:%m月%d日}".format(finish)

    return closing_date,period

# 提出日確認ボタンが押された時
def check_shift(token):
    result = next_friday()
    line_bot_api.push_message(token, TextSendMessage(text="次の締切日は"+result[0]+"です。"))
    line_bot_api.push_message(token, TextSendMessage(text=result[1]+"のシフトを提出してください。"))

# send.pyが実行された時に登録されているユーザーにメッセージ送信
def send_message():
    # db.pyから登録ユーザー取得
    get_token = db.get_user()
    # 取得したデータをループで回して全員にメッセージをPUSHする
    for token in get_token:
        check_shift(token)

if __name__ == "__main__":
    app.run()
