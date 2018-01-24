# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20180124_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='desc',
            field=models.CharField(verbose_name='商品简介', max_length=128),
        ),
    ]
