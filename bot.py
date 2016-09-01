import telebot
import config
from datetime import datetime
from db import r

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message, "Hi")


def arrive_filter(message):
    message = message.split()
    if len(message) != 2:
        return False


@bot.message_handler(commands=['create'])
def handle_create(message):
    msg = message.text.split()
    if len(msg) != 2:
        bot.reply_to(message, "Usage: /create <party_name>")
        return
    party_name = msg[1]
    print("Attempt to create party named " + party_name)
    if party_name in r.smembers('parties'):
        bot.reply_to(message, "Sorry, but there is a party with such name.")
        return
    else:
        r.sadd('parties', party_name)
        r.hmset('parties:' + party_name, {
            'owner_id': str(message.from_user.id),
            'created_at': str(datetime.utcnow())
        })
        bot.reply_to(message, "Success. Wish you good partying!")
        return


@bot.message_handler(commands=['choose'])
def handle_choose(message):
    msg = message.text.split()
    if len(msg) != 2:
        bot.reply_to(message, "Usage: /choose <party_name>")
        return
    party_name = msg[1]
    if party_name in r.smembers('parties'):
        print(message)
        r.hset('user:' + str(message.from_user.id), 'current-party',
               party_name)
        bot.reply_to(message, "Current party is " + party_name)
        return
    else:
        bot.reply_to(message, "Sorry, there is no such party")
        return

#@bot.message_handler(commands=['invite'])
#def handle_invite(message):
#r.sadd('parties:' + party_name + ':members')


@bot.message_handler(commands=['arrive'])
def handle_arrive(message):
    bot.reply_to(message, message)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.polling()
