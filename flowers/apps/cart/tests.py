from django.contrib.auth.models import User
from django.test import TestCase, Client

from apps.cart.cart import Cart
from apps.cart.forms import CartAddProductForm
from apps.cart.services import add_product_in_cart, update_quantity, delete_product_from_cart, history_orders, \
    liked_products
from apps.catalog.models import Categories
from apps.orders.forms import OrderCreateForm
from apps.orders.services import order_create
from apps.products.models import Products
from apps.products.tests import write_text, time_of_function
from apps.user.services import like_product


class TestCart(TestCase):
    """ Тестирование корзины """

    def setUp(self):
        default_time = '2000-01-01 00:00:00+03'
        my_admin = User.objects.create_superuser('root', 'vvv@gmail.com', '1111')
        Client().login(username=my_admin.username, password='1111')
        self.category = Categories(1, 'События', 'sobitiya', default_time)
        self.product1 = Products(1, 'CART', 'cart', '50000', '----', '',
                                 True, default_time, default_time, self.category.id)
        self.product1.save()
        self.category.save()
        self.user = User.objects.first()
        self.session = self.client.session
        self.session['somekey'] = 'test'
        self.session.save()

    def add_product_in_cart(self):
        form_data = {'quantity': 1}
        form = CartAddProductForm(data=form_data)
        add_product_in_cart(Cart(self), form, self.product1.id)

    @time_of_function
    def test_add_product(self):
        write_text(f'Проверка-на-добавление-товара-в-корзину')
        self.add_product_in_cart()
        for _ in Cart(self):
            print(f"Товар {_['product']} {_['price']}руб {_['quantity']} успешно добавлен")

    @time_of_function
    def test_update_quantity_product(self):
        write_text(f'Проверка-на-обновление-количества-товара-в-корзину')
        self.add_product_in_cart()
        for _ in Cart(self):
            print(f"-- Старое кол-во товара: {_['quantity']}")
            _['quantity'] = 100
        update_quantity(Cart(self))
        for _ in Cart(self):
            print(f"-- Обновленное кол-во товара: {_['quantity']}")

    @time_of_function
    def test_remove_product(self):
        write_text(f'Проверка-на-удаление-товара-в-корзину')
        self.add_product_in_cart()
        for _ in Cart(self):
            print(f"-- Товар {_['product']} удален")
        delete_product_from_cart(Cart(self), self.product1.id)

    def create_order(self):
        form_data = {'user': self.user, 'description': 'test', 'deliv_address': 'tester', 'paid': True}
        form = OrderCreateForm(data=form_data)
        if order_create('POST', Cart(self), form, self.user):
            print('--- Заказ успешно создан')
        else:
            print('--- Не удалось создать заказ')

    @time_of_function
    def test_history_orders(self):
        write_text(f'История-заказов-пользователя')
        self.create_order()
        self.create_order()
        context = history_orders({}, self.user, 1)
        for _ in context['orders']:
            order = str(_).split()
            print(f"-- №{order[0]},  Комментарий: '{order[1]}',  Адрес доставки: '{order[2]}',  "
                  f"Дата: {order[3]},  Оплата: {order[5]}")

    @time_of_function
    def test_liked_products(self):
        write_text(f'Понравившиеся-товары-пользователя')
        like_product(1, self.user)
        context = liked_products({}, self.user, 1)
        print("--- лайк успешно поставлен")
        for _ in context['products']:
            print(f'Название товара {_}')
        liked_products({}, self.user, 1)
        print("--- лайк успешно убран")
