import botsettings
import telebot
import os
from telebot import types
from flask import Flask, request

bot = telebot.TeleBot(botsettings.tg_token)
server = Flask(__name__)

def translate_string(string):
    eng_string = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?"""
    rus_string = """ёйцукенгшщзхъфывапролджэячсмитьбю.Ё!"№;%:?*()_+ЙЦУКЕНГШЩЗХЪ/ФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"""

    res_str = ""

    for s in string:
        if (eng_string.find(s) == -1):
            if (rus_string.find(s) == -1):
                res_str += s
            else:
                res_str += eng_string[rus_string.find(s)]
        else:
            res_str += rus_string[eng_string.find(s)]
    return res_str

@bot.inline_handler(func=lambda query: len(query.query) > 0)
def translate_query(query):
    res_str = translate_string(query.query)
    results = []
    single_msg = types.InlineQueryResultArticle(
        id="1", title="Gthtdtcnb", description=res_str,
        input_message_content=types.InputTextMessageContent(message_text=res_str),
        thumb_url=botsettings.thumb_url
    )
    results.append(single_msg)
    bot.answer_inline_query(query.id, results)

@bot.message_handler(commands=["start"])
def start(message):
    greet = """Z gthtrk.xf. hfcrkflre rkfdbfnehs/ Gjnjve xnj vjue/"""
    bot.send_message(message.chat.id, greet, parse_mode="Markdown")

@server.route("/" + botsettings.tg_token, methods=["POST"])
def getmessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://" + botsettings.domain + "/" + botsettings.tg_token)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    pass