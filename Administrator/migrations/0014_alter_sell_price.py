# Generated by Django 3.2.9 on 2021-12-09 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administrator', '0013_auto_20211209_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sell',
            name='price',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=10, verbose_name='交易金额'),
        ),
    ]
