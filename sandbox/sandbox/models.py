from django.db import models
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.models import Page


# See "Removal of special-purpose field panel types"
# https://docs.wagtail.org/en/stable/releases/3.0.html#removal-of-special-purpose-field-panel-types
if WAGTAIL_VERSION[0] >= 3:
    from wagtail.admin.panels import FieldPanel

    example_page_panels = [
        FieldPanel("link"),
    ]
else:
    from wagtail.snippets.edit_handlers import SnippetChooserPanel

    example_page_panels = [
        SnippetChooserPanel("link"),
    ]


class ExamplePage(Page):
    link = models.ForeignKey(
        "wagtail_links.Link",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content_panels = Page.content_panels + example_page_panels
