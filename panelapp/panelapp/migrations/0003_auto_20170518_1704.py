# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 15:58
from __future__ import unicode_literals

from django.db import migrations

def add_initial_values(apps, schema_editor):
    pass


def remove_initial_values(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('panelapp', '0002_auto_20170518_1701'),
    ]

    operations = [
        migrations.RunPython(add_initial_values, remove_initial_values)
    ]
