# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0025_skill_skill_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skillspecialization',
            name='skill_type',
        ),
        migrations.AddField(
            model_name='skillspecialization',
            name='base_skill',
            field=models.ForeignKey(to='rules.Skill', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skilltype',
            name='specialization_text',
            field=models.TextField(default='As appropriate to the type'),
        ),
    ]
