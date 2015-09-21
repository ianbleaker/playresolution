# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0007_auto_20150918_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, default='type')),
                ('type', models.CharField(choices=[('normal', 'Normal Text'), ('example', 'Play Example'), ('info', 'Information Block')], max_length=10, default='normal')),
                ('order', models.IntegerField(default=0)),
                ('content', models.TextField()),
                ('parent', models.ForeignKey(to='rules.Section')),
            ],
        ),
        migrations.CreateModel(
            name='SkillDescriptor',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('descriptor', models.CharField(choices=[('type', 'Skill Type'), ('special', 'Skill Specialization')], max_length=7, default='special')),
                ('name', models.CharField(max_length=50, default='type')),
                ('base_skill', models.ForeignKey(to='rules.Skill')),
            ],
        ),
        migrations.RemoveField(
            model_name='specialization',
            name='base_skill',
        ),
        migrations.RemoveField(
            model_name='type',
            name='base_skill',
        ),
        migrations.DeleteModel(
            name='Specialization',
        ),
        migrations.DeleteModel(
            name='Type',
        ),
    ]
