# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 14:57
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panels', '0007_auto_20170531_1122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genepanelentrysnapshot',
            options={'get_latest_by': 'created', 'ordering': ['-saved_gel_status', '-created']},
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='transcript',
        ),
        migrations.AlterField(
            model_name='activity',
            name='gene_symbol',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='phenotypes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, null=True), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='publications',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, null=True), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='rating',
            field=models.CharField(blank=True, choices=[('GREEN', 'Green List (high evidence)'), ('RED', 'Red List (low evidence)'), ('AMBER', "I don't know")], max_length=255),
        ),
        migrations.AlterField(
            model_name='trackrecord',
            name='issue_type',
            field=models.CharField(choices=[('Created', 'Created'), ('NewSource', 'Added New Source'), ('ChangedGeneName', 'Changed Gene Name'), ('SetPhenotypes', 'Set Phenotypes'), ('SetModelofInheritance', 'Set Model of Inheritance'), ('ClearSources', 'Clear Sources')], max_length=255),
        ),
    ]
