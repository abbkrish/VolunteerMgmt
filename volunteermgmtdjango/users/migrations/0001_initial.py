# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-23 06:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import phonenumber_field.modelfields
import volunteermgmtdjango.users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(default='NULL', max_length=200)),
                ('last_name', models.CharField(default='NULL', max_length=200)),
                ('email', models.EmailField(default='test@test.com', max_length=254, unique=True)),
                ('street_address_1', models.CharField(default='NULL', max_length=200)),
                ('street_address_2', models.CharField(default='NULL', max_length=200)),
                ('city', models.CharField(default='South Orange', max_length=200)),
                ('state', models.CharField(default='NJ', max_length=200)),
                ('zipcode', models.CharField(default='NULL', max_length=200)),
                ('need_community_svc_hrs', models.BooleanField(default=False)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128)),
                ('volunteer_group', models.CharField(default='NULL', max_length=200)),
                ('emergency_name', models.CharField(default='NULL', max_length=200)),
                ('emergency_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128)),
                ('waiver_filed', models.BooleanField(default=False)),
                ('other', models.CharField(default='NULL', max_length=200)),
                ('password', models.CharField(default='NULL', max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', volunteermgmtdjango.users.models.UserManager()),
            ],
        ),
    ]
