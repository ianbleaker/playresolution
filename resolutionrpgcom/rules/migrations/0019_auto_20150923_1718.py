# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0018_section_depth_string'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='depth_string',
            field=models.CharField(null=True, max_length=100, blank=True),
        ),
    ]
