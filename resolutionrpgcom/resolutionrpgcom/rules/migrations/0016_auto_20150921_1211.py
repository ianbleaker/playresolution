# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0015_auto_20150920_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='type',
            field=models.CharField(max_length=2, choices=[('n', 'Normal Text'), ('ex', 'Play Example'), ('i', 'Information Block')], default='n'),
        ),
    ]
