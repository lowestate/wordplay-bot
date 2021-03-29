import telebot
import random
import requests
bot = telebot.TeleBot('1690283667:AAEGTMTotS1h5lzhQjKfKs0_i9qglSkUsCU')

current_word = ''
count = 1
words = []
used_words = []
meaning_word = ''
count_for_victory = 0
markup = telebot.types.InlineKeyboardMarkup()
markup.add(telebot.types.InlineKeyboardButton(text='Правила', callback_data='rules'))
markup.add(telebot.types.InlineKeyboardButton(text='Старт!', callback_data='go'))

f = open('существительные.txt', encoding='utf-8')
for word in range(34010):
    file = f.readline()
    file = file[0:len(file)-1]
    words.append(file)

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('/start', 'СТОП')
levels = telebot.types.InlineKeyboardMarkup()
levels.add(telebot.types.InlineKeyboardButton(text='Легкий', callback_data='easy'))
levels.add(telebot.types.InlineKeyboardButton(text='Средний', callback_data='medium'))
levels.add(telebot.types.InlineKeyboardButton(text='Сложный', callback_data='hard'))
levels.add(telebot.types.InlineKeyboardButton(text='Бесконечный', callback_data='endless'))

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот, с которым можно играть в слова.", reply_markup=keyboard)
    bot.send_message(message.chat.id, 'Выбери режим игры: ', reply_markup=levels)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global count, used_words, count_for_victory
    bot.answer_callback_query(callback_query_id=call.id)
    answer = ''
    if call.data == 'rules':
        answer = 'Правила довольно просты: мы по очереди пишем друг другу слова, которые начинаются с последней буквы предущего слова. Например, ты напишешь "каркаС", тогда я напишу "СоловеЙ" и так далее. \nЕсли значение какого-то слова будет не понятно, то нажмите на кнопку "Значение" под этим словом. \nЧтобы закончить игру, напишите большими буквами "СТОП".'
    elif call.data == 'go':
        answer = 'Начинаем! Пиши слово.'
        used_words = []
        count = 1
    elif call.data == 'no':
        answer = 'Хорошо, удачи!'
    elif call.data == 'yes':
        bot.send_message(call.message.chat.id, 'Выбери режим игры: ', reply_markup=levels)
    elif call.data == 'easy':
        bot.send_message(call.message.chat.id, 'Для победы тебе нужно 10 раз поддержать игру правильным словом.', reply_markup=markup)
        count_for_victory = 10
    elif call.data == 'medium':
        bot.send_message(call.message.chat.id, 'Для победы тебе нужно 20 раз поддержать игру правильным словом.', reply_markup=markup)
        count_for_victory = 20
    elif call.data == 'hard':
        bot.send_message(call.message.chat.id, 'Для победы тебе нужно 30 раз поддержать игру правильным словом.', reply_markup=markup)
        count_for_victory = 30
    elif call.data == 'endless':
        bot.send_message(call.message.chat.id, 'Удачи!', reply_markup=markup)
        count_for_victory = -1
    bot.send_message(call.message.chat.id, answer)

@bot.message_handler(content_types=['text'])
def actions(message):
    global count, current_word, meaning_word, count_for_victory
    if message.text != 'СТОП' and count == 1:
        current_word = message.text[0]
        count = 0
    if message.text != 'СТОП' and count_for_victory != 0:
        for k in range(len(message.text) - 1):
            if not message.text[k].isalpha() and message.text[k] != ' ':
                message.text = message.text[0:k] + message.text[k+1:len(message.text)]
                bot.send_message(message.chat.id, 'Ваше слово содержит странные символы. Мы их обрежем и получим "' + message.text + '"')
        for j in range(len(message.text) - 1, 0, -1):
            if message.text[j] == ' ':
                bot.send_message(message.chat.id, 'Вы ввели больше одного слова. В игру принимается первое, то есть "' + message.text[0:j] + '"')
                message.text = message.text[0:j]
                break
        if (message.text[len(message.text) - 1]).lower() == 'ь':
            bot.send_message(message.chat.id, 'Вы ввели слово, которое оканчивается на мягкий знак. Я возьму предыдущую букву, то есть "' + message.text[len(message.text) - 2] + '"')
            letter = (message.text[len(message.text) - 2]).lower()
        elif (message.text[len(message.text) - 1]).lower() == 'ы':
            bot.send_message(message.chat.id, 'Вы ввели слово, которое оканчивается на "ы". Я возьму предыдущую букву, то есть "' + message.text[len(message.text) - 2] + '"')
            letter = (message.text[len(message.text) - 2]).lower()
        elif (message.text[len(message.text) - 1]).lower() == 'ъ':
            bot.send_message(message.chat.id, 'Вы ввели слово, которое оканчивается на твердый знак. Я возьму предыдущую букву, то есть "' + message.text[len(message.text) - 2] + '"')
            letter = (message.text[len(message.text) - 2]).lower()
        else:
            letter = (message.text[len(message.text) - 1]).lower()
        if message.text[0].lower() == current_word[len(current_word) - 1].lower() and count_for_victory != 0:
            mas_with_words = []
            count_for_victory -= 1
            url = 'https://ru.wiktionary.org/wiki/' + message.text.lower()
            request = requests.get(url)
            if (request.status_code == 200) and (not used_words.__contains__(str(message.text.lower()))):
                for i in range(len(words)):
                    word_from_list = words[i]
                    if letter.lower() == word_from_list[0].lower() and word_from_list[len(word_from_list)-1] != 'ь' and word_from_list[len(word_from_list)-1] != 'ы' and not used_words.__contains__(str(word_from_list.lower())):
                        mas_with_words.append(word_from_list)
                current_word = mas_with_words[random.randint(0, len(mas_with_words))]
                meaning_word = current_word[0].upper() + current_word[1:len(current_word)]
                markup_meaning = telebot.types.InlineKeyboardMarkup()
                markup_meaning.add(telebot.types.InlineKeyboardButton(text='Значение', url='https://ru.wikipedia.org/wiki/' + meaning_word))
                bot.send_message(message.chat.id, meaning_word, reply_markup=markup_meaning)
                used_words.append(str(message.text.lower()))
                used_words.append(str(current_word.lower()))
            elif request.status_code != 200:
                bot.send_message(message.chat.id, 'Кажется, слова "' + message.text + '" нет в русском языке.\nПопробуйте другое слово)')
            elif used_words.__contains__(str(message.text.lower())):
                bot.send_message(message.chat.id, 'Слово "' + message.text + '" уже было.\nПопробуйте еще раз)')
        elif message.text[0].lower() != current_word[len(current_word) - 1].lower():
            bot.send_message(message.chat.id, 'Вы ввели слово, которое начинается с буквы "' + message.text[0] + '", а нужно с буквы "' + current_word[len(current_word) - 1] + '".\nПопробуйте еще раз)')
    elif count_for_victory == 0:
        bot.send_message(message.chat.id, 'Поздравляю! Вы победили.')
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        keyboard1.add(telebot.types.InlineKeyboardButton(text='Да, давай!', callback_data='yes'))
        keyboard1.add(telebot.types.InlineKeyboardButton(text='В другой раз', callback_data='no'))
        bot.send_message(message.from_user.id, 'Cыграем еще раз?', reply_markup=keyboard1)
        count = 0
    elif message.text == 'СТОП':
        keyboard1 = telebot.types.InlineKeyboardMarkup()
        keyboard1.add(telebot.types.InlineKeyboardButton(text='Да, давай!', callback_data='yes'))
        keyboard1.add(telebot.types.InlineKeyboardButton(text='В другой раз', callback_data='no'))
        bot.send_message(message.from_user.id, 'Победила дружба :)\nCыграем еще раз?', reply_markup=keyboard1)
        count = 0
        count_for_victory = 0
        used_words.clear()

bot.polling(none_stop=True)