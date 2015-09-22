# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0004_auto_20150916_1338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trait',
            old_name='traitRequisite',
            new_name='trait_requisite',
        ),
        migrations.AddField(
            model_name='trait',
            name='race_requisite',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
