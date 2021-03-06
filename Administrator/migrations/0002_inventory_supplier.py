# Generated by Django 3.2.9 on 2021-11-21 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administrator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(default='', max_length=15, verbose_name='型号')),
                ('storage', models.IntegerField(default='0', verbose_name='库存量')),
                ('supplier', models.CharField(default='', max_length=25, verbose_name='供货商')),
                ('note', models.CharField(default='', max_length=30, verbose_name='备注(不超过30个字)')),
            ],
            options={
                'db_table': 'inventory',
            },
        ),
        migrations.CreateModel(
            name='supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=25, verbose_name='供货公司')),
                ('address', models.CharField(default='', max_length=35, verbose_name='供货商地址')),
                ('mobile', models.CharField(default='', max_length=11, verbose_name='联系方式')),
                ('type', models.CharField(default='', max_length=50, verbose_name='供货类型')),
                ('note', models.CharField(default='', max_length=30, verbose_name='备注(不超过30个字)')),
            ],
            options={
                'db_table': 'supplier',
            },
        ),
    ]
