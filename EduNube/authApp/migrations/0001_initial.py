# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-12 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=255, unique=True)),
                ('expires', models.BooleanField(default=False)),
                ('expire_date', models.DateTimeField(default=None)),
                ('secret_key', models.CharField(max_length=80, unique=True)),
                ('token', models.CharField(max_length=80)),
            ],
        ),
    ]
