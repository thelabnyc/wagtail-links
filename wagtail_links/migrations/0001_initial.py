# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0033_remove_golive_expiry_help_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
                ('link_relative', models.URLField(blank=True, verbose_name='External link')),
                ('django_view_name', models.CharField(blank=True, help_text='Name of django view for reverse lookup', max_length=255)),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
            ],
        ),
    ]
