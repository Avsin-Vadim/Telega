from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import random, pymorphy2

reg_echo = False
reg_numbers = False
reg_words = False
reg_tictactoe = False
numb = 1
print(722)
alf = ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ', 'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж',
       'э', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', 'ё']
x = "X"
o = "O"
win = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def start(bot, update):
    update.message.reply_text(
        "Привет, друг! \nДавай поиграем! Напиши мне "
        "/help, и я раскажу тебе о своих играх :D")


def help(bot, update):
    update.message.reply_text(
        "Хочешь поиграть? Прекпасно! \n"
        "/numbers и мы будем считать до бесконечности\n"
        "/words — поиграем в слова\n"
        "/tictactoe — крестики-нолики\n"
        "/echo — и я скажу всё, что скажешь ты\n"
        "/stop — и мы прекратим играть")


def echo(bot, update):
    global reg_echo, reg_numbers, reg_words, reg_tictactoe
    reg_numbers = False
    reg_words = False
    reg_tictactoe = False
    reg_echo = True


def numbers(bot, update):
    global reg_echo, reg_numbers, reg_words, reg_tictactoe, numb
    reg_echo = False
    reg_words = False
    reg_tictactoe = False
    reg_numbers = True
    numb = 1
    update.message.reply_text("В этой игре надо вводить числа, \n"
                              "которые будутут на единицу больше предыдущего")
    update.message.reply_text("Я начну")
    update.message.reply_text(numb)


def words(bot, update):
    global reg_echo, reg_numbers, reg_words, reg_tictactoe
    global k, t, za, zagad, nelza, morph, word
    reg_echo = False
    reg_words = True
    reg_tictactoe = False
    reg_numbers = False
    f = open('text.txt', 'r')
    word = f.read().split()
    k = 0
    t = 0
    za = random.choice(word)

    zagad = []
    nelza = []
    nelza.append(za)
    f.close()
    morph = pymorphy2.MorphAnalyzer()
    update.message.reply_text("Ну что ж, давай сыграем\n"
                              "Тебе же правила игры в слова объяснять не надо?\n"
                              "Тогда приступимю. Я начинаю")
    update.message.reply_text(za)


def tictactoe(bot, update):
    global reg_echo, reg_numbers, reg_words, reg_tictactoe
    global board, hod, to
    reg_echo = False
    reg_words = False
    reg_tictactoe = True
    reg_numbers = False
    board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    hod = 1
    to = 0
    update.message.reply_text("УРРРА! Крестики нолики! :D")
    update.message.reply_text("Ты ходишь первым")
    dos = 'ᅠ{} | {} | {}\n' \
          '---------------\n' \
          'ᅠ{} | {} | {}\n' \
          '---------------\n' \
          'ᅠ{} | {} | {}\n'.format(board[0], board[1], board[2], board[3], board[4], board[5], board[6], board[7],
                                   board[8], )
    update.message.reply_text(dos)


def game(bot, update):
    global reg_echo, reg_numbers, reg_words, reg_tictactoe, numb
    global k, t, za, zagad, nelza, morph, word
    global x, o, board, win, hod, pole, to

    ###NUMBERS###
    if reg_numbers:
        if update.message.text.isdigit():
            if int(update.message.text) == numb + 1:
                numb = numb + 2
                update.message.reply_text(numb)
            else:
                update.message.reply_text("Неправильное число, учись считать")
        else:
            update.message.reply_text("Вводи, пожалуйста, только числа")
    ###ECHO###
    elif reg_echo:
        update.message.reply_text(update.message.text)

    ###WORDS###
    elif reg_words:
        clovo = update.message.text
        if clovo.isalpha():
            clovo = clovo.lower()
            if clovo not in nelza:
                if za[-1] == clovo[0] or ((za[-1] == 'ь' or za[-1] == 'ы') and za[-2] == clovo[0]):
                    for bu in clovo:
                        if bu not in alf:
                            k = k + 1
                    if k == 0:
                        p = morph.parse(clovo)[0]
                        p = p.tag.cyr_repr
                        p = p.split(',')
                        if p[0] == 'СУЩ' and p[-1] == 'им':
                            if clovo in word:
                                word.remove(clovo)
                            nelza.append(clovo)
                            for sl in word:
                                if sl[0] == clovo[-1] or (
                                        (clovo[-1] == 'ь' or clovo[-1] == 'ы') and clovo[-2] == sl[0]):
                                    zagad.append(sl)
                            if zagad != []:
                                za = random.choice(zagad)
                                nelza.append(za)
                                word.remove(za)
                                update.message.reply_text(za)

                            else:
                                update.message.reply_text("Сдаюсь\n"
                                                          "Игра окончена")
                                stop(bot, update)
                        else:
                            update.message.reply_text('Слово должно быть существительным\n '
                                                      'в иминительном падеже')
                    else:
                        update.message.reply_text("Это точно на русском?")
                else:
                    update.message.reply_text("Буква не подходит")
            else:
                update.message.reply_text("Слово уже было")
        else:
            update.message.reply_text("Должны быть только буквы")
        k = 0
        zagad = []

    ###TICTACTOE###
    elif reg_tictactoe:
        global hod
        if ' ' in board:

            pole = update.message.text
            if hod == 1:

                if pole.isdigit():
                    pole = int(pole)
                    pole = pole - 1
                    if -1 < pole < 9:
                        if board[pole] == ' ':
                            board[pole] = x
                            hod = 2
                            dos = 'ᅠ{} | {} | {}\n' \
                                  '---------------\n' \
                                  'ᅠ{} | {} | {}\n' \
                                  '---------------\n' \
                                  'ᅠ{} | {} | {}\n'.format(board[0], board[1], board[2], board[3], board[4], board[5],
                                                           board[6],
                                                           board[7],
                                                           board[8], )
                            for w in win:
                                if board[w[0]] == board[w[1]] == board[w[2]] == x:
                                    if to == 0:
                                        update.message.reply_text("Ты победил(")
                                        update.message.reply_text("Игра окончена")
                                        to = 1
                                    dos = 'ᅠ{} | {} | {}\n' \
                                          '---------------\n' \
                                          'ᅠ{} | {} | {}\n' \
                                          '---------------\n' \
                                          'ᅠ{} | {} | {}\n'.format(board[0], board[1], board[2], board[3], board[4],
                                                                   board[5], board[6],
                                                                   board[7],
                                                                   board[8], )

                                    stop(bot, update)
                                elif board[w[0]] == board[w[1]] == board[w[2]] == o:
                                    if to == 0:
                                        update.message.reply_text(
                                            "Роботы вновь доказали своё превосходство над человеком!")
                                        update.message.reply_text("Игра окончена")
                                        to = 1
                                    stop(bot, update)
                            update.message.reply_text(dos)
                        else:
                            update.message.reply_text("Поле занято")
                    else:
                        update.message.reply_text("Выходишь за границы")
                else:
                    update.message.reply_text("Только цифры")

            if hod == 2:
                pole = random.randint(0, 8)
                if board[pole] == ' ':
                    board[pole] = o
                    hod = 1
                    dos = 'ᅠ{} | {} | {}\n' \
                          '---------------\n' \
                          'ᅠ{} | {} | {}\n' \
                          '---------------\n' \
                          'ᅠ{} | {} | {}\n'.format(board[0], board[1], board[2], board[3], board[4], board[5], board[6],
                                                   board[7],
                                                   board[8], )
                    update.message.reply_text(dos)
                    if to == 0:
                        update.message.reply_text("Твой ход. Выбери поля (1-9):")
                else:
                    game(bot, update)

            for w in win:
                if board[w[0]] == board[w[1]] == board[w[2]] == x:
                    if to == 0:
                        update.message.reply_text("Ты победил(")
                        update.message.reply_text("Игра окончена")
                        to = 1
                    dos = 'ᅠ{} | {} | {}\n' \
                          '---------------\n' \
                          'ᅠ{} | {} | {}\n' \
                          '---------------\n' \
                          'ᅠ{} | {} | {}\n'.format(board[0], board[1], board[2], board[3], board[4], board[5], board[6],
                                                   board[7],
                                                   board[8], )

                    stop(bot, update)
                elif board[w[0]] == board[w[1]] == board[w[2]] == o:
                    if to == 0:
                        update.message.reply_text("Роботы вновь доказали своё превосходство над человеком!")
                        update.message.reply_text("Игра окончена")
                        to = 1
                    stop(bot, update)

        else:
            for w in win:
                if board[w[0]] == board[w[1]] == board[w[2]] == x:
                    update.message.reply_text("Ты победил(")
                    update.message.reply_text("Игра окончена")
                    dos = 'ᅠ{} | {} | {}\n' \
                          '---------------\n' \
                          'ᅠ{} | {} | {}\n' \
                          '---------------\n' \
                          'ᅠ{} | {} | {}\n'.format(board[0], board[1], board[2], board[3], board[4], board[5], board[6],
                                                   board[7],
                                                   board[8], )

                    stop(bot, update)
                elif board[w[0]] == board[w[1]] == board[w[2]] == o:
                    if to == 0:
                        update.message.reply_text("Роботы вновь доказали своё превосходство над человеком!")
                        update.message.reply_text("Игра окончена")
                        to = 1
                    stop(bot, update)

                else:
                    if to == 0:
                        update.message.reply_text("Ты победил(")
                        update.message.reply_text("Игра окончена")
                        to = 1
                    stop(bot, update)


def stop(bot, update):
    global reg_echo, reg_numbers, reg_words, reg_tictactoe, numb
    reg_echo = False
    reg_numbers = False
    reg_words = False
    reg_tictactoe = False
    numb = 1


def main():
    updater = Updater("782530720:AAFNg0mmm2nWw6p6_NGj-baqpkJt2KhTGEU")

    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, game)
    dp.add_handler(text_handler)

    dp.add_handler(CommandHandler("numbers", numbers))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("echo", echo))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("words", words))
    dp.add_handler(CommandHandler("tictactoe", tictactoe))

    print(16234)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
