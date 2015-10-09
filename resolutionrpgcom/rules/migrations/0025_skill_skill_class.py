# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0024_auto_20151008_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='skill_class',
            field=models.CharField(max_length=6, choices=[('info', 'Information'), ('social', 'Social'), ('active', 'Active'), ('combat', 'Combat')], default='info'),
            preserve_default=False,
        ),
    ]
