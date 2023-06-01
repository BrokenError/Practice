from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from apps.products.models import Products, Reviews, Comments


class Profile(models.Model):
    username = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    bio = models.TextField('О себе', null=True, max_length=1000, blank=True)
    birth_date = models.DateField('День рождение', null=True, blank=True)
    profile_img = models.ImageField('Фото профиля', null=True, blank=True, upload_to="users/profile/")
    country = models.TextField('Страна', max_length=100, null=True, blank=True)
    city = models.TextField('Город', max_length=168, null=True, blank=True)
    phoneNumber = PhoneNumberField('Номер телефона', unique=True, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    balance = models.DecimalField('Баланс', max_digits=8, decimal_places=2, blank=True, default=0)


@receiver(post_save, sender=User)
def create_user_profile(instance, created,  **kwargs):
    if created:
        Profile.objects.create(username=instance)


@receiver(post_save, sender=User)
def save_user_profile(instance, **kwargs):
    instance.user_profile.save()


class ReplyComments(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    date = models.DateTimeField('Дата ответа', auto_now=True)
    text = models.TextField('Сообщение', max_length=5000)
    product = models.ForeignKey(Products, related_name='product', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, related_name='review', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.comment} {self.user} {self.date} {self.text} {self.product}'

    class Meta:
        verbose_name = "Ответ на комментарий"
        verbose_name_plural = "Ответы на комментарии"
