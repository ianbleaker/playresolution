# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0026_auto_20151008_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilltype',
            name='specialization_text',
            field=models.CharField(max_length=200, default='As appropriate to the type'),
        ),
    ]
