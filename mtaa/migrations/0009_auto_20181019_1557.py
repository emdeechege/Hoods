# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-19 12:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mtaa', '0008_auto_20181018_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='comments',
            name='post',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='user',
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='body',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='user',
        ),
        migrations.AddField(
            model_name='posts',
            name='posted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='business',
            name='b_photo',
            field=models.ImageField(null=True, upload_to='business/'),
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='mtaa.Posts'),
        ),
        migrations.AddField(
            model_name='comment',
            name='poster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]