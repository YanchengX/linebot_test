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
    'Un/J4DSchKvjhWr8uvEmXUKOowijPJCpiWU77iZxRxa8PgTRiBtrk4CHhlog7DGtHBh3t7Ato6+Bh+j43UPaTfSs6SireSV0dhnAFM+xqcR4neWzcZtzcksdub+lWtsugybkeCproHycuDT9vRUGggdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7cd651ab928ae756ce8225a6696a4a50')


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


if __name__ == "__main__":
    app.run()
