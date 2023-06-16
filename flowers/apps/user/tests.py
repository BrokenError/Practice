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
from apps.user.services import like_product, delete_user, reply_comment
from apps.user.forms import RegisterUserForm, ReplyCommentsForm


class TestUsers(TestCase):
    """ Тестирование пользователя"""
    @classmethod
    def setUp(cls):
        my_admin = User.objects.create_superuser('root', 'vvv@gmail.com', '1111')
        Client().login(username=my_admin.username, password='1111')
        cls.default_time = '2000-01-01 00:00:00+03'
        # cls.comment = Comments.objects.first()
        cls.user = User.objects.first()
        cls.client = Client()

    def test_delete_user(self):
        write_text(f'Удаление-пользователя')
        delete_user(self.user.id)
        print('Данный пользователь удален')

    def test_create_user(self):
        write_text(f'Создание-пользователя')
        my_admin = User.objects.create_superuser('tested', 'vvv@gmail.com', '1111')
        my_admin.save()
        print(f'--- Пользователь успешно создан {User.objects.get(username="tested")}')

# TODO finish the tests
    def test_reply_comment(self):
        write_text(f'Ответный-комментарий-пользователя')
        form_data = {'user': self.user, 'description': 'test', 'deliv_address': 'tester', 'paid': True}
        reply_comment(ReplyCommentsForm(data=form_data), self.user.id, 1, 1)
        ...