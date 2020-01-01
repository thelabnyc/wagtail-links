# Generated by Django 2.2.9 on 2020-01-01 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_links', '0005_auto_20191203_1908_squashed_0006_auto_20191204_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='title',
            field=models.CharField(blank=True, help_text='Description of link for use in ARIA compliance', max_length=200, verbose_name='Title'),
        ),
    ]