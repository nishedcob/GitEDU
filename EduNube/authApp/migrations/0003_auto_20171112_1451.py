# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-12 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0002_auto_20171112_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apitoken',
            name='token',
            field=models.CharField(max_length=200),
        ),
    ]
