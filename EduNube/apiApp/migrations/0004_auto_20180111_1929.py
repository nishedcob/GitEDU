# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-11 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0003_auto_20171227_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repospec',
            name='token',
            field=models.CharField(max_length=1600, unique=True),
        ),
    ]
