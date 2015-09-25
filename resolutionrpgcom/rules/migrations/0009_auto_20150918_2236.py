# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0008_auto_20150918_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='section',
            name='terse',
            field=models.TextField(null=True),
        ),
    ]
