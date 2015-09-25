# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0017_auto_20150923_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='depth_string',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
