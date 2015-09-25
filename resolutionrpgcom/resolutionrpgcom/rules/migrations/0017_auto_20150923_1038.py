# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0016_auto_20150921_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='section',
            name='type',
            field=models.CharField(max_length=2, choices=[('n', 'Normal'), ('ex', 'Example'), ('i', 'Information Block')], default='n'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='section',
            order_with_respect_to=None,
        ),
    ]
