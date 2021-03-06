# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-04 21:36
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='about_below',
            field=tinymce.models.HTMLField(blank=True, help_text=b'Onderste gedeelte over FairBlogs op de about pagina.', verbose_name='About Us'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='about',
            field=tinymce.models.HTMLField(blank=True, help_text=b'Bovenste gedeelte over FairBlogs op de about pagina.', verbose_name='About Us'),
        ),
    ]
