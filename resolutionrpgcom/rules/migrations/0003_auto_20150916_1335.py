# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0002_auto_20150916_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='trait',
            name='short_description',
            field=models.CharField(default='short_description', max_length=200),
        ),
        migrations.AlterField(
            model_name='trait',
            name='description',
            field=models.CharField(max_length=1000),
        ),
    ]
