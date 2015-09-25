# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0006_auto_20150918_1932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='derivedstatistic',
            name='statistic',
        ),
        migrations.AddField(
            model_name='statistic',
            name='derived',
            field=models.ForeignKey(to='rules.DerivedStatistic', null=True, blank=True),
        ),
    ]
