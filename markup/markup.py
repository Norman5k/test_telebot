# импортируем специальные типы телеграм бота для создания элементов интерфейса
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
# импортируем настройки и утилиты
from settings import config
# импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """
    # инициализация разметки

    def __init__(self):
        self.markup = None
        # инициализируем менеджер для работы с БД
        self.BD = DBManager()

    def set_btn(self, name, step=0, quantity=0, user_id=0):
        """
        Создает и возвращает кнопку по входным параметрам
        """

        if name == "AMOUNT_ORDERS":
            config.KEYBOARD["AMOUNT_ORDERS"] = "{} {} {}".format(step + 1,
                                                                 ' из ',
                                                                 str(self.BD.count_rows_order(user_id)))
        if name == "AMOUNT_PRODUCT":
            config.KEYBOARD["AMOUNT_PRODUCT"] = "{}".format(quantity)

        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        """
        Создает разметку кнопок в основном меню и возвращает разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('CHOOSE_GOODS')
        itm_btn_2 = self.set_btn('INFO')
        itm_btn_3 = self.set_btn('SETTINGS')
        # расположение кнопок в меню
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3)
        return self.markup

    def info_menu(self):
        """
        Создает разметку кнопок в меню info
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        # расположение кнопок в меню
        self.markup.row(itm_btn_1)
        return self.markup

    def settings_menu(self):
        """
        Создает разметку кнопок в меню settings
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        # расположение кнопок в меню
        self.markup.row(itm_btn_1)
        return self.markup

    def category_menu(self):
        """
        Создает разметку кнопок в меню категорий товара и возвращает разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True, row_width=1)
        self.markup.add(self.set_btn('SEMIPRODUCT'))
        self.markup.add(self.set_btn('GROCERY'))
        self.markup.add(self.set_btn('ICE_CREAM'))
        self.markup.row(self.set_btn('<<'),self.set_btn('ORDER'))
        return self.markup

    def set_inline_btn(self, name):
        """
        Создает и возвращает инлайн кнопку по входным параметрам
        """
        return InlineKeyboardButton(str(name),
                                    callback_data=str(name.id))

    def set_select_category(self, category):
        """
        Создает разметку инлайн кнопок в выбранной категории товара и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        # Загружаем в название инлайн кнопок данные
        # с БД в соответствии с категорией товара
        for item in self.BD.select_all_products_category(category):
            self.markup.add(self.set_inline_btn(item))

        return self.markup

    def orders_menu(self, step, quantity, user_id):
        """
        Создает разметку кнопок в заказе товара и возвращает разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn1 = self.set_btn('X', step, quantity)
        itm_btn2 = self.set_btn('DOUWN', step, quantity)
        itm_btn3 = self.set_btn('AMOUNT_PRODUCT', step, quantity)
        itm_btn4 = self.set_btn('UP', step, quantity)

        itm_btn5 = self.set_btn('BACK_STEP', step, quantity)
        itm_btn6 = self.set_btn('AMOUNT_ORDERS', step, quantity, user_id)
        itm_btn7 = self.set_btn('NEXT_STEP', step, quantity)
        itm_btn8 = self.set_btn('APPLAY', step, quantity)
        itm_btn9 = self.set_btn('<<', step, quantity)
        # расположение кнопок в меню
        self.markup.row(itm_btn1, itm_btn2, itm_btn3, itm_btn4)
        self.markup.row(itm_btn5, itm_btn6, itm_btn7)
        self.markup.row(itm_btn8, itm_btn9)
        return self.markup