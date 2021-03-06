##
## Copyright (c) 2016-2019 Genomics England Ltd.
##
## This file is part of PanelApp
## (see https://panelapp.genomicsengland.co.uk).
##
## Licensed to the Apache Software Foundation (ASF) under one
## or more contributor license agreements.  See the NOTICE file
## distributed with this work for additional information
## regarding copyright ownership.  The ASF licenses this file
## to you under the Apache License, Version 2.0 (the
## "License"); you may not use this file except in compliance
## with the License.  You may obtain a copy of the License at
##
##   http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing,
## software distributed under the License is distributed on an
## "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
## KIND, either express or implied.  See the License for the
## specific language governing permissions and limitations
## under the License.
##
# Generated by Django 2.0.8 on 2018-08-21 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("panels", "0065_auto_20180820_1006")]

    operations = [
        migrations.RemoveField(
            model_name="genepanelentrysnapshot", name="type_of_variants"
        ),
        migrations.AlterField(
            model_name="region",
            name="haploinsufficiency_score",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "3",
                        "Sufficient evidence suggesting dosage sensitivity is associated with clinical phenotype",
                    ),
                    (
                        "2",
                        "Emerging evidence suggesting dosage sensitivity is associated with clinical phenotype",
                    ),
                    (
                        "1",
                        "Little evidence suggesting dosage sensitivity is associated with clinical phenotype",
                    ),
                    (
                        "0",
                        "No evidence to suggest that dosage sensitivity is associated with clinical phenotype",
                    ),
                    ("40", "Dosage sensitivity unlikely"),
                    ("30", "Gene associated with autosomal recessive phenotype"),
                ],
                max_length=2,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="region",
            name="triplosensitivity_score",
            field=models.CharField(
                blank=True,
                choices=[
                    (
                        "3",
                        "Sufficient evidence suggesting dosage sensitivity is associated with clinical phenotype",
                    ),
                    (
                        "2",
                        "Emerging evidence suggesting dosage sensitivity is associated with clinical phenotype",
                    ),
                    (
                        "1",
                        "Little evidence suggesting dosage sensitivity is associated with clinical phenotype",
                    ),
                    (
                        "0",
                        "No evidence to suggest that dosage sensitivity is associated with clinical phenotype",
                    ),
                    ("40", "Dosage sensitivity unlikely"),
                    ("30", "Gene associated with autosomal recessive phenotype"),
                ],
                max_length=2,
                null=True,
            ),
        ),
    ]
