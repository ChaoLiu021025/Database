# Generated by Django 3.2.9 on 2021-12-10 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='name',
            field=models.CharField(default='', max_length=20, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='type',
            field=models.CharField(default='', max_length=20, verbose_name='型号'),
        ),
    ]
