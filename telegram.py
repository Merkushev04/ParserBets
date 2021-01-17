import telepot

token = '1212716658:AAFMEBth1fyC-miiafHV8rSIRwNaMgMAGEE'
chat_id = -1001401097236
telegramBot = telepot.Bot(token)


def send_message(text):
    telegramBot.sendMessage(chat_id, text, parse_mode="Markdown")