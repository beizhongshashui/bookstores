# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180123_0237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('recipient_name', models.CharField(max_length=20, verbose_name='收件人')),
                ('recipient_addr', models.CharField(max_length=256, verbose_name='收货地址')),
                ('zip_code', models.CharField(max_length=6, verbose_name='邮政编码')),
                ('recipient_phone', models.CharField(max_length=11, verbose_name='手机号码')),
                ('is_default', models.BooleanField(verbose_name='是否默认', default=False)),
                ('passport', models.ForeignKey(to='user.Passport', verbose_name='账户')),
            ],
            options={
                'db_table': 's_uer_adress',
            },
        ),
    ]
