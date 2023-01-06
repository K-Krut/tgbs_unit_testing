from football_bot.date_parser import DateParser
from football_bot.date_parser import check_date
from football_bot.team_parser import TeamParser
from football_bot.team_parser import check_team
import unittest


class TestLogic(unittest.TestCase):
    def test_date_check(self):
        self.assertEqual(False, check_date('22.10.199'.split('.')))
        self.assertNotEqual(True, check_date('2022-10-12'.split('.')))
        self.assertEqual(True, check_date('11.11.2022'.split('.')))

    def test_get_leagues(self):
        date_parser = DateParser('2022-11-11')
        self.assertEqual(['Российская футбольная Премьер-лига', 'Итальянская Серия А',
                          'Немецкая Бундеслига', 'Французская Лига 1',
                          'Эредивизи', 'Чемпионшип', 'Турецкая Суперлига'],
                         date_parser.get_leagues()
                         )

        self.assertNotEqual(['Российская футбольная Премьер-лига'], date_parser.get_leagues())
        self.assertNotEqual([], date_parser.get_leagues())

    def test_add_emoji(self):
        date_parser = DateParser('2022-11-11')
        self.assertEqual(['⚽ 🇷🇺 Российская футбольная Премьер-лига', '⚽ 🇮🇹 Итальянская Серия А',
                          '⚽ 🇩🇪 Немецкая Бундеслига', '⚽ 🇫🇷 Французская Лига 1', '⚽ 🇳🇱 Эредивизи',
                          '⚽  Чемпионшип', '⚽  Турецкая Суперлига'],
                         date_parser.leagues
                         )

    def test_matches(self):
        date_parser = DateParser('2022-11-11')
        self.assertEqual("""19:00	*Пари Нижний Новгород*	3️⃣ : 2️⃣	*Ахмат*	
	Завершен22:45	*Эмполи*	2️⃣ : 0️⃣	*Кремонезе*	
	Завершен22:30	*Боруссия М*	4️⃣ : 2️⃣	*Боруссия Дортмунд*	
	Завершен23:00	*Лион*	1️⃣ : 1️⃣	*Ницца*	
	Завершен22:00	*Спарта Роттердам*	1️⃣ : 1️⃣	*Твенте*	
	Завершен23:00	*Бирмингем Сити*	1️⃣ : 2️⃣	*Сандерленд*	
	Завершен20:00	*Аланьяспор*	0️⃣ : 0️⃣	*Адана Демиспор*	
	Завершен20:00	*Анкарагюджю*	1️⃣ : 1️⃣	*Трабзонспор*	
	Завершен""",
                         ''.join([str(i) for i in date_parser.get_matches()])
                         )

        self.assertNotEqual("""Завершен20:00	*Аланьяспор*	0️⃣ : 0️⃣	*Адана Демиспор*	
	Завершен20:00	*Анкарагюджю*	1️⃣ : 1️⃣	*Трабзонспор*	
	Завершен""", ''.join([str(i) for i in date_parser.get_matches()]))
        self.assertNotEqual("", ''.join([str(i) for i in date_parser.get_matches()]))


