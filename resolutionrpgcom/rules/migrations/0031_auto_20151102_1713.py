# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0030_auto_20151102_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trait',
            name='race_requisite',
        ),
        migrations.RemoveField(
            model_name='trait',
            name='trait_requisite',
        ),
        migrations.AddField(
            model_name='trait',
            name='requirements',
            field=models.TextField(null=True, max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='trait',
            name='value',
            field=models.CharField(default=10, max_length=20),
        ),
    ]
