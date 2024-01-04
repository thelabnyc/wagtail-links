# Generated by Django 2.1.8 on 2019-04-11 21:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import wagtail_links.models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtail_links", "0003_auto_20170522_2015"),
    ]

    operations = [
        migrations.AddField(
            model_name="link",
            name="name",
            field=models.SlugField(
                help_text="Unique name for this link (for use by Django templates).",
                null=True,
                unique=True,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="link",
            name="django_view_name",
            field=models.CharField(
                blank=True,
                help_text="Name of Django view for reverse lookup",
                max_length=255,
                validators=[wagtail_links.models.validate_django_reverse],
            ),
        ),
        migrations.AlterField(
            model_name="link",
            name="link_external",
            field=models.URLField(
                blank=True, help_text="Absolute URL Link", verbose_name="External link"
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
                verbose_name="Relative link",
            ),
        ),
    ]
