# Generated by Django 3.2.9 on 2021-11-26 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administrator', '0005_remove_inventory_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=25, verbose_name='经销公司')),
                ('address', models.CharField(default='', max_length=35, verbose_name='经销商地址')),
                ('mobile', models.CharField(default='', max_length=11, verbose_name='联系方式')),
                ('type', models.CharField(default='', max_length=50, verbose_name='需货类型')),
                ('note', models.CharField(default='', max_length=30, verbose_name='备注(不超过30个字)')),
            ],
            options={
                'db_table': 'agent',
            },
        ),
    ]