from typing import Any, Protocol, Tuple
import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.urls import NoReverseMatch, reverse
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from .fields import NullSlugField

logger = logging.getLogger(__name__)


def validate_django_reverse(view_name: str) -> None:
    try:
        reverse(view_name)
    except NoReverseMatch:
        # Translators: CMS error message
        raise ValidationError(_("Invalid Django view name"))


class LinkResolver(Protocol):
    def get_descr(self, link: "Link") -> str: ...  # NOQA: E704

    def get_url(  # NOQA: E704
        self,
        link: "Link",
        localized: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> str: ...


class LinkManager(models.Manager["Link"]):
    def get_by_natural_key(self, name: str) -> "Link":
        return self.get(name=name)


@register_snippet
class Link(index.Indexed, models.Model):
    """
    A generic link that points somewhere else using various methods
    """

    title = models.CharField(
        _("Title"),
        max_length=200,
        blank=True,
        help_text=_("Description of link for use in ARIA compliance"),
    )
    name = NullSlugField(
        _("Name"),
        unique=True,
        help_text=_("Unique name for this link (for use by Django templates)."),
    )
    link_external = models.URLField(
        _("External Link"), blank=True, help_text=_("Absolute URL Link")
    )
    link_relative = models.CharField(
        _("Relative Link"),
        max_length=200,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*",
                message="Not valid relative url",
            )
        ],
        help_text=_("Relative URL Link"),
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name=_("Wagtail Page Link"),
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
        help_text=_("Wagtail Page Link"),
    )
    django_view_name = models.CharField(
        _("Django View Link"),
        max_length=255,
        blank=True,
        validators=[validate_django_reverse],
        help_text=_("Name of Django view for reverse lookup"),
    )

    objects = LinkManager()

    panels = [
        FieldPanel("title"),
        FieldPanel("name"),
        FieldPanel("link_external"),
        FieldPanel("link_relative"),
        PageChooserPanel("link_page"),
        FieldPanel("django_view_name"),
    ]

    search_fields = [
        index.RelatedFields(
            "link_page",
            [
                index.AutocompleteField("title"),
            ],
        ),
        index.AutocompleteField("title"),
    ]

    class Meta(TypedModelMeta):
        # Translators: Internal Model Name (singular)
        verbose_name = _("Link")
        # Translators: Internal Model Name (plural)
        verbose_name_plural = _("Links")

    def natural_key(self) -> Tuple[str]:
        return (self.name,)

    def __str__(self) -> str:
        return self.get_resolver().get_descr(self)

    @property
    def url(self) -> str:
        """Get URL for use in template"""
        return self.get_url()

    def clean(self) -> None:
        # Don't allow multiple link types to be used
        number_used = (
            bool(self.link_external)
            + bool(self.link_relative)
            + bool(self.link_page)
            + bool(self.django_view_name)
        )
        if number_used > 1:
            raise ValidationError(_("You may only use one link type"))
        if number_used == 0:
            raise ValidationError(_("You must use exactly one link type"))

    def get_resolver(self) -> LinkResolver:
        conf: dict[str, Any] = getattr(
            settings,
            "WAGTAIL_LINKS",
            {},
        )
        resolver_path: str = conf.get(
            "RESOLVER",
            "wagtail_links.resolver.DefaultLinkResolver",
        )
        resolver_opts: dict[str, Any] = conf.get("RESOLVER_OPTIONS", {})
        Resolver: type[LinkResolver] = import_string(resolver_path)
        return Resolver(**resolver_opts)

    def get_url(self, *args: Any, **kwargs: Any) -> str:
        resolver = self.get_resolver()
        return resolver.get_url(self, *args, **kwargs)
