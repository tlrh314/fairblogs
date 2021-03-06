# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0002_blogger_email_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogger',
            name='facebook',
            field=models.URLField(blank=True, null=True, verbose_name='Facebook'),
        ),
        migrations.AddField(
            model_name='blogger',
            name='instagram',
            field=models.URLField(blank=True, null=True, verbose_name='Instagram'),
        ),
        migrations.AddField(
            model_name='blogger',
            name='twitter',
            field=models.URLField(blank=True, null=True, verbose_name='Twitter'),
        ),
    ]
