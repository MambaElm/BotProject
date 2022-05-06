# Импортируем необходимые классы.
import logging
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from random import shuffle

reply_keyboard = [['/start', '/help'],
                  ['/rules', '/play']]
data = {"games": {}}
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5117310045:AAFYo3gezbScZtQ5gXQy-shhT-DJ_d5uzDo'


# Функция базового ответа на любой запрос, который не предусмотрен
def base(update, context):
    update.message.reply_text(
        "Пожалуйста, напишите команду правильно, я вас не понимаю.\nНапишите /help чтобы узнать какие есть команды")


# функция приветствия нового пользователя
def start(update, context):
    update.message.reply_text(
        "Привет! Я бот для организации коммуникативных игр. Пока что я умею играть только в Киллера, но я еще учусь. Напишите /help чтобы узнать больше",
        reply_markup=markup)


def newgame(update, context):
    a = str(update.message.chat.id)
    s = str(update.message.chat.username)
    s1 = str(update.message.chat.first_name)
    if a not in data:
        data[a] = {'name': s1, 'username': s}
    b = str(update.message.text)[9:]
    if b in data['games']:
        update.message.reply_text("Игра с таким идентификатором уже есть, выберите другой идентификатор",
                                  reply_markup=markup)
    else:
        data['games'][b] = {'master': a, 'players': [], 'listplayers': []}
        h = "Игра успешно создана\nИдентификатор игры: " + b
        update.message.reply_text(h, reply_markup=markup)


def startkiller(update, context, b):
    a = data['games'][b]['players']
    shuffle(a)
    la = len(a)
    for i in range(la):
        k = (i+1)%la
        print(data, k)
        update.message.chat.id = int(a[i][0])
        h = 'Игра с идентификатором '+b+' началась\nВаша первая жертва имеет пользовательский идентификатор @'+a[k][1]+' и имя '+a[k][2]
        update.message.reply_text(h, reply_markup=markup)




def startgame(update, context):
    a = str(update.message.chat.id)
    b = str(update.message.text)[11:]
    if b in data['games']:
        if data['games'][b]['master'] == a:
            startkiller(update, context, b)
            update.message.reply_text("Игра успешно начинается",
                                      reply_markup=markup)
        else:
            update.message.reply_text("Вы не являетесь создателем игры, а потому не можете ее начать",
                                      reply_markup=markup)
    else:
        update.message.reply_text("Игры с таким идентификатором не существует", reply_markup=markup)


def endgame(update, context):
    a = str(update.message.chat.id)
    b = str(update.message.text)[9:]
    if b in data['games']:
        if data['games'][b]['master'] == a:
            update.message.reply_text("Игра успешно завершена",
                                      reply_markup=markup)
        else:
            update.message.reply_text("Вы не являетесь создателем игры, а потому не можете ее завершить",
                                      reply_markup=markup)
    else:
        update.message.reply_text("Игры с таким идентификатором не существует", reply_markup=markup)


def play(update, context):
    a = str(update.message.chat.id)
    s = str(update.message.chat.username)
    s1 = str(update.message.chat.first_name)
    if a not in data:
        data[a] = {'name': s1, 'username': s}
    b = str(update.message.text)[6:]
    if b in data['games']:
        print(data)
        if a in data["games"][b]['listplayers']:
            update.message.reply_text("Вы уже играете в эту игру", reply_markup=markup)
        else:
            data['games'][b]['listplayers'].append(a)
            data['games'][b]['players'].append((a, s, s1, 0))
            update.message.reply_text("С присоединением к игре", reply_markup=markup)
    else:
        update.message.reply_text(
            "Пожалуйста, напишите команду правильно, я вас не понимаю.\n '/play идентификатор' правильное написание данной команды\n /help — узнать другие команды",
            reply_markup=markup)


# функция чтобы узнать правила игры
def rules(update, context):
    update.message.reply_text(
        "1)Каждый участник получает имя своей цели от бота в личные сообщения. \n2)Каждый игрок является одновременно и охотником и жертвой.\n3)Чтобы убить человека необходимо дотронуться до него и  произнести ключевую фразу «Ты убит». Убийство должно быть совершено без каких-либо свидетелей. Рядом (в области видимости или в радиусе 50 метров) не должно быть ни участников игры, ни обычных людей.\n4)Если вас убили, вы обязаны переслать всех своих жертв (даже тех, кого вы уже убили) своему убийце.\n5)Если осталось в живых всего двое, и они оба знают об этом, или остался всего 1 человек игра завершается\nP.S. Это один из вариантов правил и вы можете играть по своим.",
        reply_markup=markup)


# ункция помощи со списком основных команд
def help(update, context):
    update.message.reply_text(
        "Бот может выполнить несколько команд:\n/rules — узнать правила игры киллер\n/newgame * — создать игру с уникальным идентификатором *\n/startkillergame * — начать игру киллер с идентификаторм *, команда работает только у создателя игры\n/play * — участвовать в игре с идентификатором *",
        reply_markup=markup)


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text & ~Filters.command, base)
    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("play", play))
    dp.add_handler(CommandHandler("newgame", newgame))
    dp.add_handler(CommandHandler("startgame", startgame))
    dp.add_handler(CommandHandler("endgame", endgame))
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
