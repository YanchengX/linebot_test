from flask import Flask, request, abort
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="吃我大便"))


LINE_BOT_CHANNEL_TOKEN
LINE_BOT_CHANNEL_SECRET
if __name__ == "__main__":
    app.run()
