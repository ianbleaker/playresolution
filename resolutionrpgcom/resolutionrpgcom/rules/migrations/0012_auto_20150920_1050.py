# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0011_auto_20150920_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='terse',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='title',
            field=models.CharField(max_length=50, default='Section Title'),
        ),
    ]
