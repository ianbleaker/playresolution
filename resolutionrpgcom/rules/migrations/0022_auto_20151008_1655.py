# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0021_auto_20151008_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='specializations',
            field=models.ManyToManyField(null=True, blank=True, to='rules.SkillSpecialization'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='types',
            field=models.ManyToManyField(null=True, blank=True, to='rules.SkillType'),
        ),
    ]
