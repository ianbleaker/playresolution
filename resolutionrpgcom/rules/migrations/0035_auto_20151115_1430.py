# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0034_auto_20151112_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='cost',
            field=models.CharField(null=True, max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='short_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='sub_category',
            field=models.CharField(null=True, max_length=50, blank=True),
        ),
    ]
