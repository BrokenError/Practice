from django.contrib.auth.models import User
from django.test import TestCase, Client

from apps.catalog.models import Categories
from apps.catalog.services import show_categories, search_magazine
from apps.products.models import Products
from apps.products.services import grade_product
from apps.products.tests import write_text, time_of_function, write_product


class TestCatalog(TestCase):
    """ Тестирование каталога с товарами """
    def setUp(self):
        self.default_time = '2000-01-01 00:00:00+03'
        my_admin = User.objects.create_superuser('root', 'vvv@gmail.com', '1111')
        Client().login(username=my_admin.username, password='1111')
        self.user = User.objects.first()

    def create_check_categories(self):
        data_categories = {1: ['Букеты', 'byketi'], 2: ['Цветы', 'cveti'],
                           3: ['События', 'sobitiya'], 4: ['Другое', 'drygoe']}
        for _ in data_categories:
            self.category = Categories(id=_, title=data_categories[_][0], slug=data_categories[_][1],
                                       date=self.default_time).save()

    def create_products(self):
        data_products = {1: [1, 'ТЕСТ1', 'TEST1', '1234', 1], 2: [2, 'ТЕСТ3', 'TEST3', '6500', 3]}
        for data in data_products.values():
            self.product = Products(data[0], data[1], data[2], data[3], '---', '',
                 True, self.default_time, self.default_time, data[4])
            print(f'--: {self.product.cat} ', end='')
            self.product.save()
            write_product(self)

    @time_of_function
    def test_magazine_catalog(self):
        write_text('Проверка-товаров-в-каталоге')
        self.create_check_categories()
        self.create_products()

    @time_of_function
    def test_rating_products(self):
        write_text('Проверка-рейтинга-товаров-в-каталоге')
        write_categories('добавление')
        self.create_check_categories()
        self.create_products()
        select_category = Categories.objects.get(id=1)
        grade_form_data = ['5 1', '5 2']
        for _ in grade_form_data:
            grade_product(self.user, _)

        context = show_categories(slug=select_category.slug)
        write_categories(f'выбрана - {select_category.title}')
        for prod_id in context['prod_rating']:
            print(f"-- Номер товара: {prod_id}, Оценка: {context['prod_rating'][prod_id]}")

    def test_search_in_catalog(self):
        self.create_check_categories()
        self.create_products()
        write_text("Поиск товаров в каталоге")
        text_search = 'те'
        print(f"-- Текст для поиска: {text_search}")
        print(f"---- Результат поиска:")
        context = search_magazine(text_search)
        for product in context['prod']:
            self.product.title = product
            write_product(self)


def write_categories(cat_title):
    return print('---- Категория {}'.format(cat_title))
