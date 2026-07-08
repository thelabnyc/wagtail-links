import logging

from wagtail import hooks
from wagtail.snippets.views.snippets import SnippetViewSet

from .forms import LinkForm
from .models import Link

logger = logging.getLogger(__name__)
print("HEY")


class LinkViewSet(SnippetViewSet):
    model = Link
    creation_form_class = LinkForm
    # Optional: Customize other attributes like icon, list_display, etc.


def register_link_snippet():
    logger.info("Registering Link snippet via SnippetViewSet\n")
    return LinkViewSet(
        name="link",
        url_prefix="links",
    )


hooks.register("register_snippet", register_link_snippet)
