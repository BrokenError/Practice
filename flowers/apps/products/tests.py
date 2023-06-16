import time

from django.contrib.auth.models import User
from django.db.models import Avg
from django.test import TestCase, Client

from apps.catalog.models import Categories
from apps.products.forms import ReviewForm, CommentForm
from apps.products.models import Products, Reviews, Comments, Rating
from apps.products.services import fill_form, grade_product


def time_of_function(function):
    def wrapped(*args, **kwargs):
        start_time = time.perf_counter()
        res = function(*args, **kwargs)
        print("Время выполнения: {0:.4f} сек".format(time.perf_counter() - start_time))
        return res
    return wrapped


class TestProducts(TestCase):
    """ Тестирование приложения с товарами"""
    @classmethod
    def setUp(cls):
        my_admin = User.objects.create_superuser('root', 'vvv@gmail.com', '1111')
        Client().login(username=my_admin.username, password='1111')
        cls.default_time = '2000-01-01 00:00:00+03'
        cls.comment = Comments.objects.first()
        cls.user = User.objects.first()
        cls.client = Client()

    def create_category(self):
        self.category = Categories(1, 'Букеты', 'byketi', self.default_time)
        self.category.save()
    
    def create_product(self):
        self.create_category()
        self.product = Products(1, 'ТЕСТ1', 'test', '2400', '----', '', True,
                                self.default_time, self.default_time, self.category.id)
        self.product.save()

    def add_rating(self):
        self.create_product()
        name_form_data = '5 1'
        grade_product(self.user, name_form_data)
        self.comment = Comments.objects.first()
        print('--- Рейтинг-успешно-добавлен')

    def add_comment(self):
        self.create_product()
        name_form_data = {'text': 'TEST'}
        fill_form(CommentForm(data=name_form_data), self.product, self.user)
        self.comment = Comments.objects.get(text='TEST')
        print('--- Комментарий-успешно-добавлен')

    def add_review(self):
        self.create_product()
        name_form_data = {'name': 'TESTED', 'text': 'TEST'}
        fill_form(ReviewForm(data=name_form_data), self.product, self.user)
        self.review = Reviews.objects.get(text='TEST')
        print('--- Отзыв-успешно-добавлен')

    @time_of_function
    def test_site(self):
        write_text(f"Запуск-начальной-страницы")
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        print("-- Запуск выполнен успешно")

    @time_of_function
    def test_links(self):
        write_text(f"Проверка-ссылок-страницы")
        links = ['/aboutus', '/catalog', '/user', '/cart']
        for i in links:
            response = self.client.get(i)
            self.assertEquals(response.status_code, 301)
        print("-- проверка прошла успешно")

    @time_of_function
    def test_reviews(self):
        write_text(f"Отзывы-на-товар")
        self.add_review()
        write_product(self)
        response = self.client.get(f'/reviews/{self.product.id}')
        self.assertEquals(response.status_code, 301)
        for i in self.product.check_review.all():
            print(f"-- Информация об отзыве:\n- №{i.id}, пользователь - {i.user},"
                  f" заголовок - {i.name}, содержание - {i.text}")

    @time_of_function
    def test_comments(self):
        write_text(f"Комментарии-к-товару")
        self.add_comment()
        write_product(self)
        response = self.client.get(f'/comments/{self.product.id}')
        self.assertEquals(response.status_code, 301)
        for i in self.product.check_comment.all():
            print(f"-- Информация о комментарии:\n- №{i.id}, пользователь - {i.user}, содержание: {i.text}")

    @time_of_function
    def test_remove_review(self):
        write_text(f"Удаление-отзывов")
        self.add_review()
        print(f'-- отзыв №{self.review.id} удалён')
        self.review.delete()

    @time_of_function
    def test_remove_comment(self):
        write_text(f"Удаление-комментариев")
        self.add_comment()
        print(f'-- комментарий №{self.comment.id} удален')
        self.comment.delete()

    @time_of_function
    def test_star(self):
        write_text(f"Оценка-товара")
        self.add_rating()
        write_product(self)
        print("-- Оценка: {}".format(Rating.objects.filter(prod=self.product.id)
                                     .aggregate(Avg('star')).get('star__avg')) + "/5")

    @time_of_function
    def test_change_comment(self):
        write_text("Изменение-комментария")
        self.add_comment()
        print("-- Старая информация:\n- №{}, пользователь - {}, содержание {}"
              .format(self.comment.id, self.comment.user, self.comment.text))
        changed_comment = Comments.objects.get(id=self.comment.id)
        changed_comment.text = 'CHANGED'
        print("-- Обновленная информация:\n- №{}, пользователь - {}, содержание {}"
              .format(changed_comment.id, changed_comment.user, changed_comment.text))

    @time_of_function
    def test_change_review(self):
        write_text("Изменение-отзыва")
        self.add_review()
        print("-- Старая информация:\n- №{}, пользователь - {}, содержание {}"
              .format(self.review.id, self.review.user, self.review.text))
        changed_review = Reviews.objects.get(id=self.review.id)
        changed_review.name = 'CHANGED'
        changed_review.text = 'CHANGED'
        print("-- Обновленная информация:\n- №{}, пользователь - {}, содержание {}"
              .format(changed_review.id, changed_review.user, changed_review.text))


def write_text(text):
    return print('\n' + text.center(70, "-"))


def write_product(self):
    print(f'-- Товар - {self.product.title}')
