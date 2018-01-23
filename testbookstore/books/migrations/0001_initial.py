# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('type_id', models.SmallIntegerField(default=1, verbose_name='商品种类', choices=[(1, 'Python'), (2, 'Javascript'), (3, '数据结构与算法'), (4, '机器学习'), (5, '操作系统'), (6, '数据库')])),
                ('name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('desc', models.CharField(max_length=128, verbose_name='商品价格')),
                ('unit', models.CharField(max_length=20, verbose_name='商品单位')),
                ('price', models.DecimalField(decimal_places=2, verbose_name='商品价格', max_digits=10)),
                ('stock', models.IntegerField(default=1, verbose_name='商品库存')),
                ('sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('detail', tinymce.models.HTMLField(verbose_name='商品详情')),
                ('image', models.ImageField(upload_to='books', verbose_name='商品照片')),
                ('status', models.SmallIntegerField(default=1, verbose_name='商品状态', choices=[(0, '下线'), (1, '上线')])),
            ],
            options={
                'db_table': 's_books',
            },
        ),
        migrations.CreateModel(
            name='HeroInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('hconrent', tinymce.models.HTMLField()),
            ],
        ),
    ]
