# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-12 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0003_auto_20171112_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='apitoken',
            name='edit_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='apitoken',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]