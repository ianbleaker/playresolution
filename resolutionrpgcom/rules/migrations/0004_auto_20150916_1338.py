# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0003_auto_20150916_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trait',
            name='short_description',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='trait',
            name='traitRequisite',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
