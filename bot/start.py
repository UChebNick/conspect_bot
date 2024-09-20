import time
import os
import telebot
from telebot import types
from bot import user_db
import threading
import datetime
from bot import utils
import payment
import audio2text_stack_db as stack
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.loader import token
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat.id)
    user_db.create_user(message.chat.id)
    bot.send_message(message.chat.id, 'здравствуйте вот цены на gpt https://proxyapi.ru/pricing')

# @bot.message_handler(commands=['help'])
# def help(message):
#     bot.send_message(message.chat.id, '')



@bot.message_handler(commands=['add_rubs'])
def buy_tokens(message):
    bot.send_message(message.chat.id, 'введите количество рублей')
    bot.register_next_step_handler(message, get_num_buy_tokens)

def get_num_buy_tokens(message):
    bot.send_message(message.chat.id, payment.create_invoice(int(message.text), message.chat.id)['result']['pay_url'])


available_models = {

    "gpt-3.5-turbo-1106": "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0125": "gpt-3.5-turbo-0125",
    "gpt-4": "gpt-4",
    "gpt-4-turbo": "gpt-4-turbo",
    "o1-preview": "o1-preview",
    "o1-mini": "o1-mini",
    "gpt-4o": "gpt-4o",
    "gpt-4o-2024-05-13": "gpt-4o-2024-05-13",
    "gpt-4o-2024-08-06": "gpt-4o-2024-08-06",
    "gpt-4o-mini": "gpt-4o-mini"
}


@bot.message_handler(commands=['conspect'])
def handle_conspect(message):
    chat_id = message.chat.id

    # Формируем inline-кнопки
    keyboard = types.InlineKeyboardMarkup()
    for model_name, model_id in available_models.items():
        button = types.InlineKeyboardButton(model_name, callback_data=model_id)
        keyboard.add(button)

    bot.send_message(chat_id, "Выберите нейросеть:", reply_markup=keyboard)


def handle_audio(message, selected_model):
    print(message.content_type)
    if message.content_type == 'voice':
        path = utils.save_voice(bot, message)
        id = stack.insert_data(datetime.datetime.now().timestamp(), path, None, message.chat.id, selected_model)
        print(id,99)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='нет, начать генерацию', callback_data=f'g+{id}'))

        # Отправляем сообщение с кнопками
        msg = bot.send_message(chat_id=message.chat.id,
                               text='вы можете прислать комментарии к составлению конспекта',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, handle_text, id)

    elif message.content_type == 'audio':
        try:
            path = utils.save_voice(bot, message)
            id = stack.insert_data(datetime.datetime.now().timestamp(), path, None, message.chat.id, selected_model)
            print(id)
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text='нет, начать генерацию', callback_data=f'g+{id}'))



            # Отправляем сообщение с кнопками
            msg = bot.send_message(chat_id=message.chat.id,
                             text='вы можете прислать комментарии к составлению конспекта',
                             reply_markup=keyboard)
            bot.register_next_step_handler(msg, handle_text, id)

        except:
            bot.send_message(message.chat.id, 'ошибка')

    else:
        bot.send_message(message.chat.id, 'недопустимый формат')


def handle_text(message, id):
    # if message.content_type == 'photo':
    #     photo_ids = [photo.file_id for photo in message.photo]
    #     stack.add_photo_ids(photo_ids, id)
    #     keyboard = InlineKeyboardMarkup()
    #     keyboard.add(InlineKeyboardButton(text='начать генерацию', callback_data=f'g+{id}'))
    #     # keyboard.add(InlineKeyboardButton(text='отменить добавление', callback_data=f'd+p+{id}'))
    #     # keyboard.add(InlineKeyboardButton(text='посмотреть запрос', callback_data=f'c+{id}'))
    #
    #
    #
    #     bot.send_message(message.chat.id, 'вы добавили фото', reply_markup=keyboard)

    if message.content_type == 'text':
        stack.add_comment(message.text, id)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='начать генерацию', callback_data=f'g+{id}'))
        # keyboard.add(InlineKeyboardButton(text='отменить добавление', callback_data=f'd+t+{id}'))
        # keyboard.add(InlineKeyboardButton(text='посмотреть запрос', callback_data=f'c+{id}'))
        bot.send_message(message.chat.id, 'вы добавили текст', reply_markup=keyboard)


@bot.message_handler(commands=['balance'])
def balance(message):
    bot.send_message(message.chat.id, f'ваш баланс: {user_db.get_user(message.chat.id)[1]}')

@bot.message_handler(commands=['get_conspect'])
def get_abstract(message):
    messages = stack.select_data_for_user(message.chat.id)
    for data in messages:
        if data:
            with open(f"{data[5]}.txt", "w") as f:
                f.write(data[4])
            with open(f"{data[5]}.txt", "rb") as f:
                send_doc(data[5], f)
            os.remove(f"{data[5]}.txt")
            stack.delete_by_id(data[0])
        else:
            bot.send_message('у вас нет неотправленных конспектов')



@bot.callback_query_handler(func=lambda call: call.data)
def handle_model_selection(call):
    m = call.data.split('+')
    print(m)
    if m[0] == 'g':
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        stack.update_status(m[1], 1)
        bot.send_message(call.message.chat.id, 'генерация началась')
        while True:
            if stack.get_data(call.message.chat.id, 5):
                bot.send_message(call.messge.chat.id, 'у вас недостаточно средств')

            time.sleep(2)
            bot.send_chat_action(call.message.chat.id, action='typing')
            data = stack.get_data(call.message.chat.id)

            print(data)
            if data:
                data = data[0]
                with open(f"{data[5]}.txt", "w") as f:
                    f.write(data[4])
                with open(f"{data[5]}.txt", "rb") as f:
                    send_doc(data[5], f)
                os.remove(f"{data[5]}.txt")
                stack.delete_by_id(data[0])
                break

    # elif m[0] == 'c':
    #     req = stack.
    else:
        chat_id = call.message.chat.id
        selected_model = call.data
        bot.clear_step_handler_by_chat_id(call.message.chat.id)

        bot.send_message(chat_id, f"Вы выбрали нейросеть: {call.data}. Теперь отправьте мне аудио или голосовое сообщение.")

        # Регистрируем обработчик для аудио и голосовых сообщений
        bot.register_next_step_handler(call.message, handle_audio, selected_model)

def send_message(id, text):
    bot.send_message(chat_id=id, text=text)

def send_doc(id, f):
    bot.send_document(id, f)



