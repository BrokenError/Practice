from django.contrib.auth.models import User
from django.test import TestCase, Client

from apps.catalog.models import Categories
from apps.products.forms import CommentForm
from apps.products.models import Products, Comments
from apps.products.services import fill_form
from apps.products.tests import write_text
from apps.user.forms import ReplyCommentsForm
from apps.user.models import ReplyComments
from apps.user.services import delete_user, reply_comment


class TestUsers(TestCase):
    """ Тестирование пользователя"""
    @classmethod
    def setUp(cls):
        my_admin = User.objects.create_superuser('root', 'vvv@gmail.com', '1111')
        Client().login(username=my_admin.username, password='1111')
        cls.user = User.objects.first()
        cls.client = Client()

    def add_comment(self):
        name_form_data = {'text': 'TEST'}
        fill_form(CommentForm(data=name_form_data), self.product, self.user)
        self.comment = Comments.objects.get(text='TEST')
        print('--- Комментарий-успешно-добавлен')
        return self.comment

    def test_delete_user(self):
        write_text(f'Удаление-пользователя')
        delete_user(self.user.id)
        print('Данный пользователь удален')

    def test_create_user(self):
        write_text(f'Создание-пользователя')
        my_admin = User.objects.create_superuser('tested', 'vvv@gmail.com', '1111')
        my_admin.save()
        print(f'--- Пользователь успешно создан {User.objects.get(username="tested")}')

    def test_reply_comment(self):
        default_time = '2000-01-01 00:00:00+03'
        write_text(f'Ответный-комментарий-пользователя')
        Categories(1, 'Букеты', 'byketi', default_time).save()
        self.category = Categories.objects.first()
        Products(1, 'ТЕСТ2', 'test2', '1560', '---', '',
                 True, default_time, default_time, self.category.id).save()
        self.product = Products.objects.first()
        self.comment = self.add_comment()
        reply_comment(ReplyCommentsForm(data={'text': 'test'}), self.user, self.product.id, self.comment.id)
        self.reply = ReplyComments.objects.get(id=1)
        print(f'--- Пользователь успешно создан {self.reply.user} {self.reply.text} '
              f'{self.reply.date.strftime("%Y-%m-%d %H:%M:%S")}')
