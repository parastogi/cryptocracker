# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-09 20:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0003_auto_20170909_2003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_superadmin',
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_admin',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Contests'),
        ),
    ]