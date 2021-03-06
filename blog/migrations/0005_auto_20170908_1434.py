# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-08 14:34
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20170908_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='author',
            field=models.CharField(default='admin', max_length=255),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()))),
        ),
    ]
