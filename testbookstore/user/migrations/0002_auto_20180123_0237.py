# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passport',
            name='password',
            field=models.CharField(max_length=100, verbose_name='用户密码'),
        ),
    ]
