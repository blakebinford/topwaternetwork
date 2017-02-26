# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 04:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_relation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('service_name', models.CharField(default='', max_length=125)),
                ('is_guide', models.BooleanField(default=False)),
                ('fish_location', models.CharField(max_length=80)),
                ('service_location', models.CharField(default='', max_length=80)),
                ('user_bio', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
    ]
