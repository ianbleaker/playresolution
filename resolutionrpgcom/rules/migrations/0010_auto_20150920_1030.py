# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0009_auto_20150918_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
