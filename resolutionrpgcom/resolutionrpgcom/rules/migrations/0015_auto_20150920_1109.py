# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0014_auto_20150920_1108'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={},
        ),
        migrations.RemoveField(
            model_name='section',
            name='order',
        ),
    ]
