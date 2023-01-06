from __future__ import absolute_import
import unittest

from ptbtest import UserGenerator
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import RegexHandler
from telegram.ext import Updater

from ptbtest import ChatGenerator
from ptbtest import MessageGenerator
from ptbtest import Mockbot



class TestConversationbot2(unittest.TestCase):
    def setUp(self):
        self.bot = Mockbot()
        self.cg = ChatGenerator()
        self.ug = UserGenerator()
        self.mg = MessageGenerator(self.bot)
        self.updater = Updater(bot=self.bot)

    def test_conversation(self):
        CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

        reply_keyboard = [['Поиск по дате', 'Поиск по команде', 'Помощь']]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, row_width=3)

        def start(bot, update):
            update.message.reply_text(
                "Привет! \nЭто бот для поиска футбольных матчей. \nНажми кнопку чтобы начать...",
                reply_markup=markup
            )
            return CHOOSING

        def regular_choice(update, user_data):
            text = update.message.text
            user_data['choice'] = text

            return TYPING_REPLY

        def help_(bot, update):
            update.message.reply_text(
                "Чтобы начать использование бота введите команду '/start';"
                "\nЕсли возникли проблемы — перезапустите бота и нажмите '/start';"
                "\nЧтобы посмотреть все возможности бота введите '/all_commands'.",
            )

            return CHOOSING

        def all_commands(bot, update):
            update.message.reply_text(
                "Перечень всех команд: "
                "\n/start — перезапуск бота; "
                "\n/help — инструкция использования; "
                "\n/all_commands — перечень возможных команд; "
                "\n/search_by_date — поиск матчей по дате;"
                "\n/search_by_team — поиск информации по команде;"
            )
            return CHOOSING

        def search_by_date_com(bot, update):
            update.message.reply_text("Введите дату в формате: дд.мм.гггг")

        def done(user_data):
            if 'choice' in user_data:
                del user_data['choice']

            user_data.clear()
            return ConversationHandler.END



        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start),
                          CommandHandler('help', help_),
                          CommandHandler('all_commands', all_commands),
                          CommandHandler('search_by_date', search_by_date_com),
                          ],
            states={
                CHOOSING: [RegexHandler('^(Поиск по дате|Поиск по команде|Помощь)$',
                                        regular_choice,
                                        pass_user_data=True),
                           ],
                TYPING_CHOICE: [MessageHandler(Filters.text,
                                               regular_choice,
                                               pass_user_data=True),
                                ],
            },
            fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
        )



        dp = self.updater.dispatcher
        dp.add_handler(conv_handler)
        self.updater.start_polling()

        user = self.ug.get_user()
        chat = self.cg.get_chat(user=user)




        # Тестування команди /start
        update = self.mg.get_message(user=user, chat=chat, text="/start")
        self.bot.insertUpdate(update)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'],
                         r"Привет! \nЭто бот для поиска футбольных матчей. \nНажми кнопку чтобы начать...")



        # Тестування опції вибору
        update = self.mg.get_message(user=user, chat=chat, text="Поиск по дате")
        self.bot.insertUpdate(update)
        self.assertRegex(update['message']['text'], r"^(Поиск по дате|Поиск по команде|Помощь)$")



        # Тестування команди /search_by_date
        update = self.mg.get_message(user=user, chat=chat, text="/search_by_date")
        self.bot.insertUpdate(update)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'], r"Введите дату в формате: дд.мм.гггг")



        # Тестування команди /help
        update = self.mg.get_message(user=user, chat=chat, text="/help")
        self.bot.insertUpdate(update)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'],
                         "Чтобы начать использование бота введите команду '/start';"
                         "\nЕсли возникли проблемы — перезапустите бота и нажмите '/start';"
                         "\nЧтобы посмотреть все возможности бота введите '/all_commands'.",
                         )


        # Тестування команди /all_commands
        update = self.mg.get_message(user=user, chat=chat, text="/all_commands")
        self.bot.insertUpdate(update)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'],
                         "Перечень всех команд: "
                         "\n/start — перезапуск бота; "
                         "\n/help — инструкция использования; "
                         "\n/all_commands — перечень возможных команд; "
                         "\n/search_by_date — поиск матчей по дате;"
                         "\n/search_by_team — поиск информации по команде;",
                         )


        # Тестування правильності чату
        self.assertEqual(data['chat_id'], chat.id)

        self.updater.stop()


if __name__ == '__main__':
    unittest.main()
