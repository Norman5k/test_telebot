from handlers.handler import Handler
from settings import config, utility
from settings.message import MESSAGES


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_info(self, message):
        """
        Обрабатываем входящие текстовые сообщения от нажатия на кнопку TradingStore
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.info_menu())

    def pressed_btn_settings(self, message):
        """
        Обрабатываем входящие текстовые сообщения от нажатия на кнопку settings
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.settings_menu())

    def pressed_btn_back(self, message):
        """
        Обрабатываем входящие текстовые сообщения от нажатия на кнопку back
        """
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keybords.start_menu())

    def pressed_btn_category(self, message):
        """
        Обрабатываем входящие текстовые сообщения от нажатия на кнопку Выбора товара
        """
        self.bot.send_message(message.chat.id, "Каталог категорий товара\n"
                                               "Сделайте свой выбор",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_product(self, message, product):
        """
        Обрабатываем входящие текстовые сообщения от нажатия на кнопки каталога товаров
        """
        self.bot.send_message(message.chat.id, 'Категория ' + config.KEYBOARD[product],
                              reply_markup=self.keybords.set_select_category(config.CATEGORY[product]))
        self.bot.send_message(message.chat.id,"Ok",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_order(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку Заказ
        """
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        user_id = message.chat.id
        count = self.BD.select_all_product_id(user_id)
        # получаем количество по каждой позиции товара в заказе
        quantity = self.BD.select_order_quantity(count[self.step], user_id)

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю при выполнении различных действий
        """
        user_id = message.chat.id
        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(
            self.step+1), parse_mode="HTML")
        self.bot.send_message(message.chat.id, MESSAGES['order'].format(
            self.BD.select_single_product_name(product_id),
            self.BD.select_single_product_title(product_id),
            self.BD.select_single_product_price(product_id),
            self.BD.select_order_quantity(product_id, user_id)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.orders_menu(self.step, quantity, user_id))

    def pressed_btn_up(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку UP
        """
        user_id = message.chat.id
        # получаем id всех товаров в заказе
        count = self.BD.select_all_product_id(user_id)
        # получаем количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step], user_id)
        # получаем количество кокретной позиции в продуктах
        quantity_product = self.BD.select_single_product_quantity(count[self.step])
        # если товар есть
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            # вносим изменения в БД
            self.BD.update_order_value(count[self.step], user_id, 'quantity', quantity_order)
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_douwn(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку DOUWN
        """
        user_id = message.chat.id
        # получаем id всех товаров в заказе
        count = self.BD.select_all_product_id(user_id)
        # получаем количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step], user_id)
        # получаем количество кокретной позиции в продуктах
        quantity_product = self.BD.select_single_product_quantity(count[self.step])
        # если товар есть
        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            # вносим изменения в БД
            self.BD.update_order_value(count[self.step], user_id, 'quantity', quantity_order)
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку X
        """
        # получаем id всех товаров в заказе
        user_id = message.chat.id
        count = self.BD.select_all_product_id(user_id)
        # если список не пуст
        if count.__len__() > 0:
            # получаем количество конкретной позиции в заказе
            quantity_order = self.BD.select_order_quantity(count[self.step], user_id)
            # получаем количество товара в конкретной позиции заказа для возврата в product
            quantity_product = self.BD.select_single_product_quantity(count[self.step])
            quantity_product += quantity_order
            # вносим изменения в БД
            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)
            self.BD.delete_order(count[self.step], user_id)
            # уменьшаем шаг
            if self.step > 0:
                self.step -= 1

        count = self.BD.select_all_product_id(user_id)
        # если список не пуст
        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step], user_id)
            # отправляем пользователю сообщение
            self.send_message_order(count[self.step], quantity_order, message)

        else:
            # если товара нет в заказе отправляем сообщение
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.category_menu())

    def pressed_btn_back_step(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку BACK_STEP
        """
        # уменьшаем шаг пока шаг не будет равен 0
        if self.step > 0:
            self.step -= 1
        # получаем список всех товаров в заказе
        user_id = message.chat.id
        count = self.BD.select_all_product_id(user_id)
        quantity = self.BD.select_order_quantity(count[self.step], user_id)

        # отправляем сообщение пользователю
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_next_step(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку NEXT_STEP
        """
        user_id = message.chat.id
        # увеличиваем шаг пока шаг не будет равен количеству строк полей заказа
        if self.step < self.BD.count_rows_order(user_id) - 1:
            self.step += 1
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id(user_id)
        quantity = self.BD.select_order_quantity(count[self.step], user_id)

        # отправляем сообщение пользователю
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_applay(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку Оформить заказ
        """
        user_id = message.chat.id
        self.bot.send_message(message.chat.id,
                              MESSAGES['applay'].format(
                                  utility.get_total_cost(self.BD, user_id),
                                  utility.get_total_quantity(self.BD, user_id)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.category_menu())
        # очищаем данные с заказа
        self.BD.delete_all_order(user_id)

    def handle(self):
        # обработчик (декоратор) сообщений,
        # который обрабатывает входящие текстовые сообщения от нажатия кнопок
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):

            # основное меню
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['ORDER']:
                # если есть заказ
                if self.BD.count_rows_order(message.chat.id) > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode="HTML",
                                          reply_markup=self.keybords.category_menu())

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            # подменю выбора товара
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            # подменю заказа
            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['DOUWN']:
                self.pressed_btn_douwn(message)

            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)

            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)

            if message.text == config.KEYBOARD['APPLAY']:
                self.pressed_btn_applay(message)
            # иные нажатия и ввод данных пользователем
            else:
                self.bot.send_message(message.chat.id, message.text)