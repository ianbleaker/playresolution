# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0019_auto_20150923_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='depth_string',
            field=models.CharField(max_length=19, null=True, blank=True),
        ),
    ]
