# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-07 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panels', '0033_auto_20171207_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genepanel',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='genepanel',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='genepanel',
            name='promoted',
        ),
        migrations.AlterField(
            model_name='genepanel',
            name='status',
            field=models.CharField(choices=[('promoted', 'promoted'), ('public', 'public'), ('retired', 'retired'), ('internal', 'internal'), ('deleted', 'deleted')], db_index=True, default='internal', max_length=36),
        ),
    ]