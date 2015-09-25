# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0010_auto_20150920_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='content',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='parent',
            field=models.ForeignKey(null=True, blank=True, to='rules.Section'),
        ),
    ]
