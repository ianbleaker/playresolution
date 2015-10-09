# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0020_auto_20150923_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillSpecialization',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(default='type', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SkillType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(default='type', max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='skilldescriptor',
            name='base_skill',
        ),
        migrations.AlterField(
            model_name='section',
            name='type',
            field=models.CharField(default='n', max_length=2, choices=[('n', 'Normal'), ('ex', 'Example'), ('i', 'Info Block')]),
        ),
        migrations.DeleteModel(
            name='SkillDescriptor',
        ),
        migrations.AddField(
            model_name='skill',
            name='specializations',
            field=models.ManyToManyField(to='rules.SkillSpecialization'),
        ),
        migrations.AddField(
            model_name='skill',
            name='types',
            field=models.ManyToManyField(to='rules.SkillType'),
        ),
    ]
