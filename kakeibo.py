
# -*- coding: utf-8 -*-
import os
from spredSheetsContoroller import sheetContoroller
from user import user
import traceback

from flask import Flask, request,abort
app = Flask(__name__)

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import TextSendMessage
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    FollowEvent, UnfollowEvent, MessageEvent, PostbackEvent,
    TextMessage, TextSendMessage, TemplateSendMessage,
    ButtonsTemplate, CarouselTemplate, CarouselColumn,
    PostbackTemplateAction)




LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = os.environ.get("YOUR_CHANNEL_SECRET")
AKI_ID = os.environ.get("AKI_ID")
RICO_ID = os.environ.get("RICO_ID")


line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
mode ={}

@app.route("/callback", methods=["GET", "POST"])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']   

    # リクエストボディを取得
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 署名を検証し、エラーが発生すれば例外を投げる
        abort(400)

    return 'OK'


@handler.add(MessageEvent)
def nyui(event):
    print(event.source.user_id)
    print(mode.get(event.source.user_id))

    user_id = None

    message =  event.message.text
    if message.find('りこ！') == 1:
        user_id = RICO_ID
        message.lstrip('りこ！')
    elif message.find('あき！') == 1:
        user_id = AKI_ID
        message.lstrip('りこ！')
    else:
        user_id = event.source.user_id


    try:
        if mode.get(event.source.user_id) == "spending":
            sheetContoroller.recordSpending(sheetContoroller,event.message.text,event.source.user_id)
            line_bot_api.reply_message(
                    event.reply_token,
                        TextSendMessage(text="かいたよー"))
        if mode.get(event.source.user_id) == "debt":
            sheetContoroller.recordDebt(sheetContoroller,event.message.text,event.source.user_id)
            line_bot_api.reply_message(
                    event.reply_token,
                        TextSendMessage(text="かいたよー"))
    except:
        print(traceback.format_exc())
        line_bot_api.reply_message(
                event.reply_token,
                    TextSendMessage(text="かけんかったよ"))


@handler.add(PostbackEvent)
def mode_change(event):
    print(event.postback)
    global mode
    mode[event.source.user_id] = event.postback.data
    if mode.get(event.source.user_id) == "spending":
        line_bot_api.reply_message(
            event.reply_token,
                TextSendMessage(text=f"使ったお金をめも！"))
    if mode.get(event.source.user_id) == "debt":
        line_bot_api.reply_message(
            event.reply_token,
                TextSendMessage(text=f"つけとくぞー"))
    if mode.get(event.source.user_id) == "query":
        line_bot_api.push_message(event.source.user_id, messages=TextSendMessage(text=f"かくにんするねー"))
        queryCotent = TextSendMessage(text=sheetContoroller.outPutQuery(sheetContoroller,event.source.user_id))
        line_bot_api.push_message(event.source.user_id, messages=queryCotent)
    else :
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"まだ作ってない！"))
        
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 80))
    app.run(debug=False, host='0.0.0.0', port=port)