# Generated by Django 2.1.3 on 2019-04-02 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panels', '0069_auto_20190109_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='last_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='last_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
