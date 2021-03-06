# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-21 01:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EquivalentUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lti_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equivalent_lti_user', to=settings.AUTH_USER_MODEL)),
                ('normal_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equivalent_normal_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
