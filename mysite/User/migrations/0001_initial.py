# Generated by Django 2.1.7 on 2019-02-25 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default='', max_length=200, verbose_name='用户名')),
                ('password', models.CharField(blank=True, default='e10adc3949ba59abbe56e057f20f883e', max_length=200, verbose_name='密码')),
            ],
        ),
    ]