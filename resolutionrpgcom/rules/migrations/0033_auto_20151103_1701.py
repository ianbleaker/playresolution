# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0032_auto_20151103_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trait',
            name='requirements',
        ),
        migrations.AddField(
            model_name='trait',
            name='replace_requirement',
            field=models.ManyToManyField(null=True, related_name='replace_requirement_rel_+', blank=True, to='rules.Trait'),
        ),
        migrations.AddField(
            model_name='trait',
            name='trait_requirement',
            field=models.ManyToManyField(null=True, related_name='trait_requirement_rel_+', blank=True, to='rules.Trait'),
        ),
    ]
