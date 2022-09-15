# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 15:52
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtail_links", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="link_relative",
            field=models.CharField(
                blank=True,
                max_length=200,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Not valid relative url",
                        regex="^(?!www\\.|(?:http|ftp)s?://|[A-Za-z]:\\\\|//).*",
                    )
                ],
                verbose_name="Relative link",
            ),
        ),
    ]
