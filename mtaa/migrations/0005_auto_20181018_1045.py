# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-18 07:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mtaa', '0004_auto_20181018_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='hood',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='biz', to='mtaa.Hood'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='u_hood',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='join', to='mtaa.Hood'),
        ),
    ]
