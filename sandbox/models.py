from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel


class ExamplePage(Page):
    link = models.ForeignKey(
        'wagtail_links.Link',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        SnippetChooserPanel('link'),
    ]
