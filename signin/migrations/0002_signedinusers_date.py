# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-21 02:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('signin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='signedinusers',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
