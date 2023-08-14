import telebot
from telebot import types
import db_exchange
import os
import datetime

user_dict = {}

API_TOKEN = "####"
check_flag = False
bot = telebot.TeleBot(API_TOKEN)

class User:
    def __init__(self, name):
        self.first_person = name
        self.second_person = name

@bot.message_handler(commands=['help', 'start'])
def menu(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Записать расходы")
    but2 = types.KeyboardButton("Вывести детализацию расходов")
    markup.add(but1)
    markup.add(but2)
    bot.reply_to(message, "Чем могу помочь?", reply_markup = markup)

@bot.message_handler(func=lambda message: True)
def handler(message):
    if message.text == 'Записать расходы':
        markup_family = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton('NAME1')
        but2 = types.KeyboardButton('NAME2')
        markup_family.add(but1)
        markup_family.add(but2)
        bot.reply_to(message, "Чьи расходы заполняем?", reply_markup = markup_family)
        db_exchange.create_table()

    if message.text == "Вывести детализацию расходов":
        bot.reply_to(message, db_exchange.sum_print_detalisation())


    if message.text == "NAME1":
        global name
        name = message.text
        
        alex_ask = bot.reply_to(message, 'Какую сумму вводим?')
        bot.register_next_step_handler(alex_ask, calc_handler)
    
    if message.text == "NAME2":
        name = message.text
        yana_ask = bot.reply_to(message, "Какую сумму вводим?")
        bot.register_next_step_handler(yana_ask, calc_handler)

def calc_handler(message):
    try:
        global inp
        inp = message.text

        if not inp.isdigit():
            alex_ask = bot.reply_to(message, 'Сумма должна быть целым числом без пробелов. Повторите ввод.')
            bot.register_next_step_handler(alex_ask, calc_handler)
            return
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton('Да')
        but2 = types.KeyboardButton('Нет')
        markup.add(but1, but2)
        global inp_show
        inp_show = '{0:,}'.format(int(inp)).replace(',', ' ')
        answer = bot.reply_to(message, f"""Вы ввели следующую сумму: {inp_show} рублей. Все верно?""", reply_markup = markup)
        bot.register_next_step_handler(answer, answer_process)
    except Exception as e:
        bot.reply_to(message, "Что-то сломалось :(")

def answer_process(message):
        answer = message.text
        if answer == 'Да':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            but1 = types.KeyboardButton('Да')
            but2 = types.KeyboardButton('Нет')
            markup.add(but1, but2)
            message = bot.reply_to(message, f"Расход в {inp_show} рублей был добавлен.\nВы хотите внести еще расход?")
            db_exchange.commit_expenses(name, inp)
            bot.register_next_step_handler(message, loop_func)
    
        if answer == 'Нет':
            bot.reply_to(message, 'Повторите ввод или вернитесь в меню.')

def loop_func(message):
    answer = message.text
    if answer == 'Да':
        reply = bot.reply_to(message, "Введите сумму.")
        bot.register_next_step_handler(reply, calc_handler)
    else:
        return menu(message)


bot.infinity_polling()

