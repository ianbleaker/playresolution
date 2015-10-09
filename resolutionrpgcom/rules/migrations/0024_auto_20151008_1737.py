# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0023_auto_20151008_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skillspecialization',
            name='base_skill',
        ),
        migrations.AlterField(
            model_name='skillspecialization',
            name='skill_type',
            field=models.ForeignKey(default=1, to='rules.SkillType'),
            preserve_default=False,
        ),
    ]
