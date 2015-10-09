# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0028_auto_20151008_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='skill_class',
            field=models.CharField(max_length=11, choices=[('information', 'Information'), ('social', 'Social'), ('active', 'Active'), ('combat', 'Combat')]),
        ),
        migrations.AlterField(
            model_name='skillspecialization',
            name='name',
            field=models.CharField(default='specialization', max_length=50),
        ),
    ]
