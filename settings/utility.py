
# конвертируем картеж в массив
def _convert(list_convert):
    return [itm[0] for itm in list_convert]

# подсчёт общей суммы заказа и возвращение результата
def total_cost(list_quantity, list_price):
    order_total_cost = 0

    for ind, itm in enumerate(list_price):
        order_total_cost += list_quantity[ind]*list_price[ind]

    return order_total_cost

# подсчёт общего количества заказанной единицы товара и возвращение результата
def total_quantity(list_quantity):
    order_total_quantity = 0

    for itm in list_quantity:
        order_total_quantity += itm

    return order_total_quantity

def get_total_cost(BD, user_id):
    """
    Возвращает общую стоимость товара
    """
    # получаем список всех product_id заказа
    all_product_id = BD.select_all_product_id(user_id)
    # получаем список стоимости по всем позициям заказа в виде обычного списка
    all_price = [BD.select_single_product_price(itm) for itm in all_product_id]
    # получаем список количества по всем позициям заказа в виде обычного списка
    all_quantity = [BD.select_order_quantity(itm, user_id) for itm in all_product_id]
    # возврашает общую стоимость товара
    return total_cost(all_quantity, all_price)

def get_total_quantity(BD, user_id):
    """
    Возвращает общее количество заказанной единицы товара
    """
    # получаем список всех product_id заказа
    all_product_id = BD.select_all_product_id(user_id)
    # получаем список количества по всем позициям заказа в виде обычного списка
    all_quantity = [BD.select_order_quantity(itm, user_id) for itm in all_product_id]
    # возвращает общее количество заказанной единицы товара
    return total_quantity(all_quantity)