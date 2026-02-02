import telebot
import random
from telebot import types

bot = telebot.TeleBot('8273588028:AAF95OnMSZfCNWVNK1O94XbXmJuYOdsNcjI')

# Глобальная переменная для хранения уровня пользователя
user_levels = {}
user_states = {}

# Словари для разных уровней (заполните своими данными)
A1_verbs = [
    ['beginnen (beginnt)', 'begann', 'hat begonnen'],
    ['bleiben (bleibt)', 'blieb', 'ist geblieben'],
    ['bringen (bringt)', 'brachte', 'hat gebracht'],
    ['denken (denkt)', 'dachte', 'hat gedacht'],
    ['dürfen (darf)', 'durfte', 'hat gedurft'],
    ['essen (isst)', 'aß', 'hat gegessen'],
    ['fahren (fährt)', 'fuhr', 'hat/ist gefahren'],
    ['fangen (fängt)', 'fing', 'hat gefangen'],
    ['finden (findet)', 'fand', 'hat gefunden'],
    ['fliegen (fliegt)', 'flog', 'hat/ist geflogen'],
    ['geben (gibt)', 'gab', 'hat gegeben'],
    ['gehen (geht)', 'ging', 'hat gegangen'],
    ['haben (hat)', 'hatte', 'hat gehabt'],
    ['heißen (heißt)', 'hieß', 'hat geheißen'],
    ['helfen (hilft)', 'half', 'hat geholfen'],
    ['kennen (kennt)', 'kannte', 'hat gekannt'],
    ['kommen (kommt)', 'kam', 'ist gekommen'],
    ['können (kann)', 'konnte', 'hat gekonnt'],
    ['lesen (liest)', 'las', 'hat gelesen'],
    ['mögen (mag)', 'mochte', 'hat gemocht'],
    ['müssen (muss)', 'musste', 'hat gemusst'],
    ['nehmen (nimmt)', 'nahm', 'hat genommen'],
    ['rufen (ruft)', 'rief', 'hat gerufen'],
    ['schlafen (schläft)', 'schlief', 'hat geschlafen'],
    ['schreiben (schriebt)', 'schrieb', 'hat geschrieben'],
    ['schwimmen (schwimmt)', 'schwamm', 'hat/ist geschwommen'],
    ['sehen (sieht)', 'sah', 'hat gesehen'],
    ['sein (ist)', 'war', 'hat gewesen'],
    ['singen (singt)', 'sang', 'hat gesungen'],
    ['sollen (soll)', 'sollte', 'hat gesollt'],
    ['sprechen (spricht)', 'sprach', 'hat gesprochen'],
    ['stehen (steht)', 'stand', 'hat gestanden'],
    ['treffen (trifft)', 'traf', 'hat getroffen'],
    ['trinken (trinkt)', 'trank', 'hat getrunken'],
    ['tun (tut)', 'tat', 'hat getan'],
    ['wissen (weiß)', 'wusste', 'hat gewusst'],
    ['wollen (will)', 'wollte', 'hat gewollt']
]

A2_verbs = [
    # TODO: Заполните глаголами уровня A2
    # Формат: [Infinitiv, Präteritum, Perfekt]
    # ['глагол', 'форма2', 'форма3'],
]

B1_verbs = [
    # TODO: Заполните глаголами уровня B1
    # Формат: [Infinitiv, Präteritum, Perfekt]
]

B2_verbs = [
    # TODO: Заполните глаголами уровня B2
    # Формат: [Infinitiv, Präteritum, Perfekt]
]

C1_verbs = [
    # TODO: Заполните глаголами уровня C1
    # Формат: [Infinitiv, Präteritum, Perfekt]
]

C2_verbs = [
    # TODO: Заполните глаголами уровня C2
    # Формат: [Infinitiv, Präteritum, Perfekt]
]

# Словарь для быстрого доступа к массивам глаголов по уровням
level_verbs = {
    1: A1_verbs,
    2: A2_verbs,
    3: B1_verbs,
    4: B2_verbs,
    5: C1_verbs,
    6: C2_verbs
}


@bot.message_handler(commands=["start"])
def start(m, res=False):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    # Создаем кнопки для всех уровней
    key_a1 = types.InlineKeyboardButton(text='A1', callback_data='A1')
    key_a2 = types.InlineKeyboardButton(text='A2', callback_data='A2')
    key_b1 = types.InlineKeyboardButton(text='B1', callback_data='B1')
    key_b2 = types.InlineKeyboardButton(text='B2', callback_data='B2')
    key_c1 = types.InlineKeyboardButton(text='C1', callback_data='C1')
    key_c2 = types.InlineKeyboardButton(text='C2', callback_data='C2')

    # Добавляем кнопки в клавиатуру
    keyboard.add(key_a1, key_a2, key_b1, key_b2, key_c1, key_c2)

    bot.send_message(m.chat.id, 'Привет! Выбери свой уровень немецкого языка:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    chat_id = call.message.chat.id

    # Сопоставляем callback_data с числовыми уровнями
    level_map = {
        'A1': 1,
        'A2': 2,
        'B1': 3,
        'B2': 4,
        'C1': 5,
        'C2': 6
    }

    if call.data in level_map:
        selected_level = level_map[call.data]
        user_levels[chat_id] = selected_level

        # Проверяем, есть ли слова для выбранного уровня
        verb_list = level_verbs.get(selected_level)

        if not verb_list or len(verb_list) == 0:
            level_name = call.data
            bot.send_message(chat_id,
                             f'Вы выбрали уровень {level_name}.\n'
                             f'⚠️ Словарь для этого уровня пока не заполнен.\n'
                             f'Нажми /start чтобы выбрать другой уровень.')
        else:
            bot.send_message(chat_id,
                             f'Вы выбрали уровень {call.data}.\n'
                             f'Напиши "Готов", и мы начнем упражнения!')
            user_states[chat_id] = 'waiting_for_ready'


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
    user_level = user_levels[chat_id]

    # Получаем список глаголов для текущего уровня
    verb_list = level_verbs.get(user_level)

    # Проверяем, есть ли слова для этого уровня
    if not verb_list or len(verb_list) == 0:
        bot.send_message(chat_id,
                         '⚠️ Словарь для этого уровня пока не заполнен.\n'
                         'Нажми /start чтобы выбрать другой уровень.')

        # Удаляем состояние пользователя
        if chat_id in user_states:
            del user_states[chat_id]
        return

    # Выбираем случайный глагол
    verb_num = random.randint(0, len(verb_list) - 1)

    # Выбираем случайную форму (2 или 3 для индексов 0, 1, 2)
    form = random.randint(2, 3)

    # Сохраняем правильный ответ и информацию о вопросе
    correct_answer = verb_list[verb_num][form - 1]
    base_verb = verb_list[verb_num][0]

    # Сохраняем правильный ответ в состоянии пользователя
    user_states[chat_id] = {
        'state': 'waiting_for_answer',
        'correct_answer': correct_answer,
        'form': form,
        'verb': base_verb,
        'level': user_level
    }

    # Отправляем вопрос
    level_names = {1: 'A1', 2: 'A2', 3: 'B1', 4: 'B2', 5: 'C1', 6: 'C2'}
    level_name = level_names.get(user_level, '')

    bot.send_message(chat_id, f'Уровень: {level_name}\nНапиши мне {form} форму глагола "{base_verb}"')


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
        bot.send_message(chat_id, '✅ Верно!')
    else:
        bot.send_message(chat_id, f'❌ Неверно\nПравильно: {correct_answer}')

    # Задаем следующий вопрос
    ask_question(message)


bot.polling(none_stop=True, interval=0)
