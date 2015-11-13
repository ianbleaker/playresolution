# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0033_auto_20151103_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('armor', 'Armor'), ('computers', 'Computers'), ('food', 'Food'), ('gear', 'Gear'), ('service', 'Service'), ('tech', 'Tech'), ('vehicle', 'Vehicle'), ('weapon', 'Weapon')], max_length=20)),
                ('sub_category', models.CharField(max_length=20)),
                ('cost', models.IntegerField(default=0)),
                ('short_description', models.TextField()),
                ('description', ckeditor.fields.RichTextField(null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='trait',
            name='replace_requirement',
            field=models.ManyToManyField(related_name='replace_requirement_rel_+', to='rules.Trait', blank=True),
        ),
        migrations.AlterField(
            model_name='trait',
            name='trait_requirement',
            field=models.ManyToManyField(related_name='trait_requirement_rel_+', to='rules.Trait', blank=True),
        ),
    ]
