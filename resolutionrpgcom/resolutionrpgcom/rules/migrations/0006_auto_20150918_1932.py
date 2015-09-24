# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0005_auto_20150918_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aptitude',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('short_description', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DerivedStatistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('divisor', models.IntegerField(default=5)),
                ('dividend_a', models.ForeignKey(related_name='dividend_a', to='rules.Aptitude')),
                ('dividend_b', models.ForeignKey(related_name='dividend_b', to='rules.Aptitude')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('what', models.TextField(default='what')),
                ('when', models.TextField(default='when')),
                ('base_aptitude', models.ForeignKey(to='rules.Aptitude')),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(default='specialization', max_length=50)),
                ('base_skill', models.ForeignKey(to='rules.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('short_description', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(default='type', max_length=50)),
                ('base_skill', models.ForeignKey(to='rules.Skill')),
            ],
        ),
        migrations.AlterField(
            model_name='trait',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='trait',
            name='race_requisite',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='trait',
            name='short_description',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='trait',
            name='trait_requisite',
            field=models.ForeignKey(blank=True, null=True, to='rules.Trait'),
        ),
        migrations.AddField(
            model_name='derivedstatistic',
            name='statistic',
            field=models.ForeignKey(to='rules.Statistic'),
        ),
    ]
