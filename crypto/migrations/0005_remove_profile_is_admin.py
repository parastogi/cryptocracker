# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-09 20:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0004_auto_20170909_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_admin',
        ),
    ]