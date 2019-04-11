from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse, NoReverseMatch
from wagtail.admin.edit_handlers import PageChooserPanel, FieldPanel
from wagtail.snippets.models import register_snippet
import logging

logger = logging.getLogger(__name__)


def validate_django_reverse(view_name):
    try:
        reverse(view_name)
    except NoReverseMatch:
        raise ValidationError(_('Invalid django view name'))


class LinkManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


@register_snippet
class Link(models.Model):
    """
    A generic link that points somewhere else using various methods
    """
    name = models.SlugField("Name",
        unique=True, null=True,
        help_text=_("Unique name for this link (for use by Django templates)."))
    link_external = models.URLField("External link",
        blank=True,
        help_text=_("Absolute URL Link"))
    link_relative = models.CharField(
        "Relative link",
        max_length=200,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*',
                message='Not valid relative url',
            ),
        ],
        help_text=_("Relative URL Link"))
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.CASCADE,
        help_text=_("Wagtail Page Link"))
    django_view_name = models.CharField(
        max_length=255,
        blank=True,
        validators=[
            validate_django_reverse,
        ],
        help_text=_("Name of Django view for reverse lookup"))

    objects = LinkManager()

    panels = [
        FieldPanel('name'),
        FieldPanel('link_external'),
        FieldPanel('link_relative'),
        PageChooserPanel('link_page'),
        FieldPanel('django_view_name'),
    ]


    def natural_key(self):
        return (self.name, )


    def __str__(self):
        url = self.url
        if not url:
            url = 'No Link URL'
        if self.name:
            return 'Link[name={}]: {}'.format(self.name, url)
        if self.link_external:
            return 'Link[link_external={}]: {}'.format(self.link_external, url)
        if self.link_relative:
            return 'Link[link_relative={}]: {}'.format(self.link_relative, url)
        if self.link_page:
            return 'Link[link_page={}]: {}'.format(str(self.link_page), self.url)
        return 'Link[django_view_name={}]: {}'.format(self.django_view_name, url)


    @property
    def url(self):
        """ Get URL for use in template """
        # 1. External Links
        if self.link_external:
            return self.link_external
        # 2. Relative Links
        if self.link_relative:
            return self.link_relative
        # 3. Wagtail Page Links
        if self.link_page:
            url = self.link_page.url
            if url is None:
                return ''
            return url
        # 4. Django View Links
        try:
            return reverse(self.django_view_name)
        except NoReverseMatch:
            logger.warning('Unable to reverse Django URL for Link[id=%s]', self.id)
        # 5. Error Fallback
        return ''


    def clean(self):
        # Don't allow multiple link types to be used
        number_used = bool(self.link_external) + \
            bool(self.link_relative) + \
            bool(self.link_page) + \
            bool(self.django_view_name)
        if number_used > 1:
            raise ValidationError(_('You may only use one link type'))
        if number_used == 0:
            raise ValidationError(_('You must use exactly one link type'))
