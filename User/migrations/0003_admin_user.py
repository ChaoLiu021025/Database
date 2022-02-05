# Generated by Django 3.2.9 on 2021-11-18 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_user_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'admin_user',
            },
        ),
    ]
