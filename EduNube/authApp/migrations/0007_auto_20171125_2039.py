# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-25 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0006_auto_20171112_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apitoken',
            name='edit_date_in_token',
            field=models.CharField(default='None', max_length=35),
        ),
        migrations.AlterField(
            model_name='apitoken',
            name='token',
            field=models.CharField(max_length=300),
        ),
    ]
