from flask import Flask, request, abort
import os

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

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    if text == "hello":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="hello_world"))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="bye")
        )

if __name__ == "__main__":
    app.run()
