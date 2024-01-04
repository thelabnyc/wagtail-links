# Generated by Django 2.2.8 on 2019-12-04 21:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import wagtail_links.models


class Migration(migrations.Migration):
    replaces = [
        ("wagtail_links", "0005_auto_20191203_1908"),
        ("wagtail_links", "0006_auto_20191204_2129"),
    ]

    dependencies = [
        ("wagtail_links", "0004_auto_20190411_2102"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="link",
            options={"verbose_name": "Link", "verbose_name_plural": "Links"},
        ),
        migrations.AlterField(
            model_name="link",
            name="django_view_name",
            field=models.CharField(
                blank=True,
                help_text="Name of Django view for reverse lookup",
                max_length=255,
                validators=[wagtail_links.models.validate_django_reverse],
                verbose_name="Django View Link",
            ),
        ),
        migrations.AlterField(
            model_name="link",
            name="link_external",
            field=models.URLField(
                blank=True, help_text="Absolute URL Link", verbose_name="External Link"
            ),
        ),
        migrations.AlterField(
            model_name="link",
            name="link_page",
            field=models.ForeignKey(
                blank=True,
                help_text="Wagtail Page Link",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="wagtailcore.Page",
                verbose_name="Wagtail Page Link",
            ),
        ),
        migrations.AlterField(
            model_name="link",
            name="link_relative",
            field=models.CharField(
                blank=True,
                help_text="Relative URL Link",
                max_length=200,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Not valid relative url",
                        regex="^(?!www\\.|(?:http|ftp)s?://|[A-Za-z]:\\\\|//).*",
                    )
                ],
                verbose_name="Relative Link",
            ),
        ),
        migrations.AlterField(
            model_name="link",
            name="name",
            field=models.SlugField(
                blank=True,
                help_text="Unique name for this link (for use by Django templates).",
                null=True,
                unique=True,
                verbose_name="Name",
            ),
        ),
        migrations.AddField(
            model_name="link",
            name="title",
            field=models.SlugField(
                blank=True,
                help_text="Description of link for use in ARIA compliance",
                verbose_name="Title",
            ),
        ),
    ]
