# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0029_auto_20151008_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='trait',
            name='type',
            field=models.CharField(default='background', max_length=10, choices=[('background', 'Information'), ('personality', 'Social'), ('physical', 'Active'), ('feature', 'Combat'), ('vehicle', 'Vehicle')]),
        ),
        migrations.AlterField(
            model_name='section',
            name='type',
            field=models.CharField(default='n', max_length=2, choices=[('n', 'Normal'), ('s', 'Subsection'), ('ex', 'Example'), ('i', 'Info Block')]),
        ),
        migrations.AlterField(
            model_name='skillspecialization',
            name='base_skill',
            field=models.ForeignKey(related_name='specializations', to='rules.Skill'),
        ),
        migrations.AlterField(
            model_name='skilltype',
            name='base_skill',
            field=models.ForeignKey(related_name='types', to='rules.Skill'),
        ),
    ]
