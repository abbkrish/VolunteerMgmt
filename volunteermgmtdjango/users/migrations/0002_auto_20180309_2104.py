# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-10 02:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='accept_terms',
            field=models.BooleanField(default=True),
            )
    ]
