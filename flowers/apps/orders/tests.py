from django.contrib.auth.models import User
from django.test import TestCase, Client

from apps.catalog.models import Categories
from apps.orders.forms import OrderCreateForm
from apps.orders.services import order_create
from apps.products.models import Products
from apps.products.tests import write_text, time_of_function


class TestOrders(TestCase):
    """ Тестирование системы заказов """

    def setUp(self):
        default_time = '2000-01-01 00:00:00+03'
        my_admin = User.objects.create_superuser('root', 'vvv@gmail.com', '1111')
        Client().login(username=my_admin.username, password='1111')
        self.category = Categories(1, 'Букеты', 'byketi', default_time)
        self.product1 = Products(1, 'ТЕСТ1', 'test', '2400', '----', '',
                                 True, default_time, default_time, self.category.id)
        self.product2 = Products(1, 'ТЕСТ2', 'test2', '1560', '---', '',
                                 True, default_time, default_time, self.category.id)
        self.product1.save()
        self.product2.save()
        self.category.save()
        self.user = User.objects.first()
        self.client = Client()

    @time_of_function
    def test_create_order(self):
        write_text('Создание-заказа')
        cart = [{'product': self.product1, 'price': self.product1.price, 'quantity': 1},
                {'product': self.product2, 'price': self.product2.price, 'quantity': 2}]
        form_data = {'user': self.user, 'description': 'test', 'deliv_address': 'tester', 'paid': True}
        form = OrderCreateForm(data=form_data)
        if order_create('POST', cart, form, self.user):
            print('--- Заказ успешно создан')
        else:
            print('--- Не удалось создать заказ')
        self.assertTrue(form.is_valid())
        response = self.client.get('/cart/orders/create')
        self.assertEqual(response.status_code, 301)
