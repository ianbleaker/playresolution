# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0022_auto_20151008_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='specializations',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='types',
        ),
        migrations.AddField(
            model_name='skillspecialization',
            name='base_skill',
            field=models.ForeignKey(to='rules.Skill', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skillspecialization',
            name='skill_type',
            field=models.ForeignKey(blank=True, null=True, to='rules.SkillType'),
        ),
        migrations.AddField(
            model_name='skilltype',
            name='base_skill',
            field=models.ForeignKey(to='rules.Skill', default=1),
            preserve_default=False,
        ),
    ]
