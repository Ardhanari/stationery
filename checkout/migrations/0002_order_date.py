# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-23 15:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
