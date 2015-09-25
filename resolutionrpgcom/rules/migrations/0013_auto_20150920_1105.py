# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0012_auto_20150920_1050'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='section',
            order_with_respect_to='parent',
        ),
    ]
