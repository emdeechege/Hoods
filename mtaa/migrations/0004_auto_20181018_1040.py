# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-18 07:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mtaa', '0003_auto_20181018_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='hood',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='mtaa.Hood'),
        ),
    ]
