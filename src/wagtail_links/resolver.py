from typing import Any
import logging

from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext

from .models import Link

logger = logging.getLogger(__name__)


class DefaultLinkResolver:
    def get_descr(self, link: Link) -> str:
        url = link.url
        if not url:
            url = gettext("No Link URL")
        ctx = {
            "name": link.name,
            "link_external": link.link_external,
            "link_relative": link.link_relative,
            "link_page": link.link_page,
            "django_view_name": link.django_view_name,
            "url": url,
        }
        if link.name:
            return gettext("Link[name=%(name)s]: %(url)s") % ctx
        if link.link_external:
            return gettext("Link[link_external=%(link_external)s]: %(url)s") % ctx
        if link.link_relative:
            return gettext("Link[link_relative=%(link_relative)s]: %(url)s") % ctx
        if link.link_page:
            return gettext("Link[link_page=%(link_page)s]: %(url)s") % ctx
        return gettext("Link[django_view_name=%(django_view_name)s]: %(url)s") % ctx

    def get_url(
        self,
        link: Link,
        localized: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> str:
        # 1. External Links
        if link.link_external:
            return link.link_external
        # 2. Relative Links
        if link.link_relative:
            return link.link_relative
        # 3. Wagtail Page Links
        if link.link_page:
            if localized:
                url = link.link_page.localized.url
            else:
                url = link.link_page.url
            if url is None:
                return ""
            return url
        # 4. Django View Links
        try:
            return reverse(link.django_view_name)
        except NoReverseMatch:
            logger.warning("Unable to reverse Django URL for Link[id=%s]", link.pk)
        # 5. Error Fallback
        return ""
