# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0032_auto_20171015_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrations',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Team'),
        ),
    ]
