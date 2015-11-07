# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0031_auto_20151102_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('short_description', models.CharField(max_length=200, blank=True)),
                ('description', ckeditor.fields.RichTextField(null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='trait',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='trait',
            name='type',
            field=models.CharField(max_length=15, default='background', choices=[('background', 'Background'), ('personality', 'Personality'), ('physical', 'Physical'), ('feature', 'Feature'), ('vehicle', 'Vehicle'), ('genetic', 'Genetic')]),
        ),
        migrations.AddField(
            model_name='trait',
            name='species_requirement',
            field=models.ForeignKey(null=True, to='rules.Species', blank=True),
        ),
    ]
