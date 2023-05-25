# Generated by Django 3.2.19 on 2023-05-23 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20230522_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now=True, max_length=0, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]