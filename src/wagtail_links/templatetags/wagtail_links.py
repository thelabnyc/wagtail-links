from typing import Any
import logging

from django import template

from ..models import Link

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def get_wagtail_link(link_name: str) -> Link | None:
    """
    Get a Link object by its name.
    """
    try:
        link = Link.objects.get_by_natural_key(link_name)
    except Link.DoesNotExist:
        logger.error("Wagtail Link with name [%s] does not exist.", link_name)
        return None
    return link


@register.simple_tag
def get_wagtail_link_url(
    link_name: str,
    localized: bool = True,
    *args: Any,
    **kwargs: Any,
) -> str:
    """
    Get a Link URL by its Link name.
    """
    link = get_wagtail_link(link_name)
    if link is None:
        return ""
    return link.get_url(localized=localized, *args, **kwargs)
