# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail_links.models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtail_links", "0002_auto_20170522_1552"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="django_view_name",
            field=models.CharField(
                blank=True,
                help_text="Name of django view for reverse lookup",
                max_length=255,
                validators=[wagtail_links.models.validate_django_reverse],
            ),
        ),
    ]
