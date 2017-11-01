# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panels', '0029_genepanel_deleted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='evaluation',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='trackrecord',
            name='issue_type',
            field=models.CharField(choices=[('Created', 'Created'), ('NewSource', 'Added New Source'), ('RemovedSource', 'Removed Source'), ('ChangedGeneName', 'Changed Gene Name'), ('SetPhenotypes', 'Set Phenotypes'), ('SetModelofInheritance', 'Set Model of Inheritance'), ('ClearSources', 'Clear Sources'), ('SetModeofPathogenicity', 'Set mode of pathogenicity'), ('GeneClassifiedbyGenomicsEnglandCurator', 'Gene classified by Genomics England curator'), ('SetModeofInheritance', 'Set mode of inheritance'), ('SetPenetrance', 'Set penetrance'), ('SetPublications', 'Set publications'), ('ApprovedGene', 'Approved Gene'), ('GelStatusUpdate', 'GelStatusUpdate'), ('UploadGeneInformation', 'Upload gene information'), ('RemovedTag', 'Removed Tag'), ('AddedTag', 'Added Tag')], max_length=512),
        ),
    ]
