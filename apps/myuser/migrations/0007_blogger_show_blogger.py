# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-19 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0006_auto_20170704_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogger',
            name='show_blogger',
            field=models.BooleanField(default=True, help_text='Designates whether the blogger is displayed in the list of all bloggers', verbose_name='Show in Bloggers list'),
        ),
    ]