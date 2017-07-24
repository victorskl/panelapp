# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 08:53
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panels', '0013_auto_20170614_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genepanelentrysnapshot',
            name='mode_of_pathogenicity',
            field=models.CharField(blank=True, choices=[('', 'Provide exceptions to loss-of-function'), ('Loss-of-function variants (as defined in pop up message) DO NOT cause this phenotype - please provide details in the comments', 'Loss-of-function variants (as defined in pop up message) DO NOT cause this phenotype - please provide details in the comments'), ('Other - please provide details in the comments', 'Other - please provide details in the comments')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='genepanelentrysnapshot',
            name='penetrance',
            field=models.CharField(blank=True, choices=[('unknown', 'unknown'), ('Complete', 'Complete'), ('Incomplete', 'Incomplete')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='genepanelentrysnapshot',
            name='phenotypes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='genepanelentrysnapshot',
            name='publications',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None),
        ),
    ]
