# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 10:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_reviewers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('GEL', 'GEL'), ('EXTERNAL', 'EXTERNAL'), ('REVIEWER', 'REVIEWER')], default='EXTERNAL', max_length=255)),
                ('affiliation', models.CharField(max_length=255)),
                ('workplace', models.CharField(choices=[('Research lab', 'Research lab'), ('NHS diagnostic lab', 'NHS diagnostic lab'), ('Other diagnostic lab', 'Other diagnostic lab'), ('NHS clinical service', 'NHS clinical service'), ('Other clinical service', 'Other clinical service'), ('Industry', 'Industry'), ('Other', 'Other')], max_length=255)),
                ('role', models.CharField(choices=[('Clinical Scientist', 'Clinical Scientist'), ('Clinician', 'Clinician'), ('Genome analyst', 'Genome analyst'), ('Genetic Counsellor', 'Genetic Counsellor'), ('Bioinformatician', 'Bioinformatician'), ('Industry', 'Industry'), ('Lab director', 'Lab director'), ('Principal Investigator', 'Principal Investigator'), ('Technician', 'Technician'), ('Researcher', 'Researcher'), ('Student', 'Student'), ('Other', 'Other')], max_length=255)),
                ('group', models.CharField(choices=[('GeCIP domain', 'GeCIP domain'), ('GENE consortium member', 'GENE consortium member'), ('NHS Genomic Medicine Centre', 'NHS Genomic Medicine Centre'), ('Other NHS organisation', 'Other NHS organisation'), ('Other biotech or pharmaceutical', 'Other biotech or pharmaceutical'), ('Other', 'Other')], max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='reviewers',
            name='user',
        ),
        migrations.DeleteModel(
            name='Reviewers',
        ),
    ]