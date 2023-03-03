from datetime import datetime
from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_base.dbcore import Base
from models.order import Order
from models.product import Products
from settings import config, utility


class Singleton(type):
    """
    Патерн Singleton предоставляет механизм создания одного
    и только одного объекта класса,
    и предоставление к нему глобальную точку доступа.
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """ 
    Класс менеджер для работы с БД 
    """

    def __init__(self):
        """
        Инициализация сессии и подключения к БД
        """
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_products_category(self, category):
        """
        Возвращает все строки товара категории
        """
        result = self._session.query(Products).filter_by(
            category_id=category).all()
        self.close()
        return result

    def close(self):
        # Закрываем сессию
        self._session.close()

    def _add_orders(self, quantity, product_id, user_id,):
        """
        Метод заполнения заказа
        """
        # получаем список всех product_id
        all_id_product = self.select_all_product_id(user_id)
        # если данные есть в списке, обновляем таблицы заказа и продуктов
        if product_id in all_id_product:
            quantity_order = self.select_order_quantity(product_id)
            self.update_order_value(product_id, user_id, 'quantity', quantity_order + 1)

            quantity_product = self.select_single_product_quantity(product_id)
            self.update_product_value(product_id, 'quantity', quantity_product - 1)

        # если данных нет, создаем новый объект заказа
        else:
            order = Order(quantity=quantity, product_id=product_id,
                          user_id=user_id, data=datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            self.update_product_value(product_id, 'quantity', quantity_product - 1)
            self._session.add(order)
            self._session.commit()

        self.close()

    def select_all_product_id(self, user_id):
        """
        Возвращет все id товара в заказе
        """
        result = self._session.query(Order.product_id).filter_by(user_id=user_id).all()
        self.close()
        # конвертируем результат выборки в вид [1,3,5...]
        return utility._convert(result)

    def select_order_quantity(self, product_id, user_id):
        """
        Возвращает количество товара по product_id в заказе
        """
        result = self._session.query(Order.quantity).filter_by(
            product_id=product_id, user_id=user_id).one()
        self.close()
        return result.quantity;

    def select_single_product_quantity(self, product_id):
        """
        Возвращает количество товара на складе
        в соответствии с номером товара - product_id
        Этот номер определяется при выборе товара в интерфейсе
        """
        result = self._session.query(Products.quantity).filter_by(
            id=product_id).one()
        self.close()
        return result.quantity

    def select_single_product_name(self, product_id):
        """
        Возвращает наименование товара на складе
        в соответствии с номером товара - product_id
        Этот номер определяется при выборе товара в интерфейсе
        """
        result = self._session.query(Products.name).filter_by(
            id=product_id).one()
        self.close()
        return result.name

    def select_single_product_title(self, product_id):
        """
        Возвращает заголовок товара на складе
        в соответствии с номером товара - product_id
        Этот номер определяется при выборе товара в интерфейсе
        """
        result = self._session.query(Products.title).filter_by(
            id=product_id).one()
        self.close()
        return result.title

    def select_single_product_price(self, product_id):
        """
        Возвращает цену товара на складе
        в соответствии с номером товара - product_id
        Этот номер определяется при выборе товара в интерфейсе
        """
        result = self._session.query(Products.price).filter_by(
            id=product_id).one()
        self.close()
        return result.price

    def update_order_value(self, product_id, user_id, name, value):
        """
        Обновляем данные указанной позиции заказа
        в соответствии с product_id
        """
        self._session.query(Order).filter_by(
            product_id=product_id, user_id=user_id).update({name: value})
        self._session.commit()
        self.close()

    def update_product_value(self, product_id, name, value):
        """
        Обновляем количество товара на складе
        в соответствии с product_id
        """
        self._session.query(Products).filter_by(
            id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def count_rows_order(self, user_id):
        """
        Возвращает количество позиций в заказе
        """
        result = self._session.query(Order).filter_by(user_id=user_id).count()
        self.close()
        return result

    def delete_order(self, product_id, user_id):
        """
        Удаляет данные указанной строки заказа
        """
        self._session.query(Order).filter_by(product_id=product_id, user_id=user_id).delete()
        self._session.commit()
        self.close()

    def delete_all_order(self, user_id):
        """
        Удаление данных всего заказа
        """
        all_id_orders = self.select_all_order_id(user_id)

        for itm in all_id_orders:
            self._session.query(Order).filter_by(id=itm).delete()
            self._session.commit()
        self.close()

    def select_all_order_id(self, user_id):
        """
        Возвращает все id заказа
        """
        result = self._session.query(Order.id).filter_by(user_id=user_id).all()
        self.close()
        return utility._convert(result)