from pyclbr import readmodule
from random import random
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)
from sympy import re

import random

app = Flask(__name__)

line_bot_api = LineBotApi(
    'dQuT/Pq4nvlJ1QLyIrNn1gPgn6tujeaJZPoeCxUFrstW+CxWC7No/xfmiFkCYN5KQJEcumrcqrPOy0MkQrleNXhfyN7vQRo8AgkJ1zcZObfSvw59pB/GZoSUV2EgXwyYCn59m+lXi5z3DVuJ3G42iAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d974f7b2be1c754a8c1b4aa9757715b0')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

pic = {
    1:"https://i.imgur.com/qGkmkyz.jpeg",
    2:"https://i.imgur.com/L3nyCjU.jpeg",
    3:"https://i.imgur.com/KkO494w.jpeg",
    4:"https://i.imgur.com/wxP7IzZ.jpeg",
    5:"https://i.imgur.com/hZhNuQE.jpeg",
    6:"https://i.imgur.com/g7acSxE.jpeg",
    7:"https://i.imgur.com/tmCGRBC.jpg",
    8:"https://i.imgur.com/9SaykEv.jpg",
}

pica = {
    1:"https://i.imgur.com/cwsmxFb.jpeg",
    2:"https://i.imgur.com/0gt9Xjh.jpeg",
    3:"https://i.imgur.com/YKEHp8H.jpeg",
    4:"https://i.imgur.com/Az7Jreo.jpeg",
    5:"https://i.imgur.com/lPGSaNN.jpg",
    6:"https://i.imgur.com/RFJBqWt.jpg",
}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text=="抽小豬":
        a = random.randint(1,7)
        if a in pic :
            image_message = ImageSendMessage(
                original_content_url=pic[a],
                preview_image_url=pic[a]
            )
        line_bot_api.reply_message(event.reply_token, image_message)
    elif event.message.text=="抽阿詹":
        a = random.randint(1,6)
        if a in pica :
            image_message = ImageSendMessage(
                original_content_url=pica[a],
                preview_image_url=pica[a]
            )
        line_bot_api.reply_message(event.reply_token, image_message)
    elif event.message.text=="嗨大and強":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="早安咖啡"))

if __name__ == "__main__":
    app.run()
