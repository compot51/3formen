import telebot
import random
from telebot import types

bot = telebot.TeleBot('8273588028:AAF95OnMSZfCNWVNK1O94XbXmJuYOdsNcjI')

# Глобальная переменная для хранения уровня пользователя
user_levels = {}
user_states = {}


@bot.message_handler(commands=["start"])
def start(m, res=False):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='A1', callback_data='A1')
    keyboard.add(key_yes)
    bot.send_message(m.chat.id, 'Привет, выбери свой уровень языка', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "A1":
        user_levels[call.message.chat.id] = 1
        bot.send_message(call.message.chat.id, 'Напиши "Готов", и мы начнем')
        user_states[call.message.chat.id] = 'waiting_for_ready'


@bot.message_handler(content_types=["text"])
def handle_text(message):
    chat_id = message.chat.id

    # Если пользователь еще не выбрал уровень
    if chat_id not in user_levels:
        bot.send_message(chat_id, 'Пожалуйста, сначала выберите уровень языка, нажав /start')
        return

    # Если пользователь выбрал уровень, но еще не написал "Готов"
    if user_states.get(chat_id) == 'waiting_for_ready':
        if message.text.lower() == 'готов':
            ask_question(message)
        else:
            bot.send_message(chat_id, 'Напиши "Готов", чтобы начать')
        return

    # Проверяем, есть ли у пользователя активный вопрос
    if chat_id in user_states and isinstance(user_states[chat_id], dict) and user_states[chat_id].get(
            'state') == 'waiting_for_answer':
        check_answer(message)
        return

    # Если пользователь в непонятном состоянии, задаем новый вопрос
    ask_question(message)


def ask_question(message):
    chat_id = message.chat.id

    if user_levels[chat_id] == 1:
        verb_list = [
            ['beginnen', 'begann', 'hat begonnen'],
            ['bleiben', 'blieb', 'ist geblieben'],
            ['bringen', 'brachte', 'hat gebracht'],
            ['denken', 'dachte', 'hat gedacht'],
            ['dürfen', 'durfte', 'hat gedurft'],
            ['essen', 'aß', 'hat gegessen'],
            ['fahren', 'fuhr', 'hat/ist gefahren'],
            ['fangen', 'fing', 'hat gefangen'],
            ['finden', 'fand', 'hat gefunden'],
            ['fliegen', 'flog', 'hat/ist geflogen'],
            ['geben', 'gab', 'hat gegeben'],
            ['gehen', 'ging', 'hat gegangen'],
            ['haben', 'hatte', 'hat gehabt'],
            ['heißen', 'hieß', 'hat geheißen'],
            ['helfen', 'half', 'hat geholfen']
        ]

    # Выбираем случайный глагол (0-14)
    verb_num = random.randint(0, len(verb_list) - 1)

    # Выбираем случайную форму (1, 2 или 3 для индексов 0, 1, 2)
    form = random.randint(2, 3)

    # Сохраняем правильный ответ и информацию о вопросе
    correct_answer = verb_list[verb_num][form - 1]
    base_verb = verb_list[verb_num][0]

    # Сохраняем правильный ответ в состоянии пользователя
    user_states[chat_id] = {
        'state': 'waiting_for_answer',
        'correct_answer': correct_answer,
        'form': form,
        'verb': base_verb
    }

    # Отправляем вопрос
    bot.send_message(chat_id, f'Напиши мне {form} форму глагола "{base_verb}"')


def check_answer(message):
    chat_id = message.chat.id

    # Проверяем, есть ли активный вопрос
    if chat_id not in user_states or not isinstance(user_states[chat_id], dict):
        ask_question(message)
        return

    user_data = user_states[chat_id]
    user_answer = message.text.strip()
    correct_answer = user_data['correct_answer']

    if user_answer.lower() == correct_answer.lower():
        bot.send_message(chat_id, 'Верно! ✅')
    else:
        bot.send_message(chat_id, f'Неверно ❌\nПравильный ответ: {correct_answer}')

    # Задаем следующий вопрос
    ask_question(message)


bot.polling(none_stop=True, interval=0)
