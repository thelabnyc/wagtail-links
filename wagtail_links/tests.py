from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.template import Context, Template
from django.test import override_settings
from wagtail.models import Page
from wagtail.search import index
from wagtail.search.backends import get_search_backend
from wagtail.test.utils import WagtailPageTests

from .models import DEFAULT_SEARCH_FIELDS, Link


class WagtailLinksSearchFieldsResolutionTest(WagtailPageTests):
    """Unit-level checks of how the WAGTAIL_LINKS_SEARCH_FIELDS setting resolves."""

    def test_defaults_when_setting_unset(self):
        self.assertEqual(Link.get_search_fields(), list(DEFAULT_SEARCH_FIELDS))

    @override_settings(WAGTAIL_LINKS_SEARCH_FIELDS=[index.AutocompleteField("testname")])
    def test_uses_setting_when_set(self):
        self.assertEqual([f.field_name for f in Link.get_search_fields()], ["testname"])

    @override_settings(WAGTAIL_LINKS_SEARCH_FIELDS=[])
    def test_empty_list_is_respected(self):
        # An explicit empty list means "no searchable fields" (contract).
        self.assertEqual(Link.get_search_fields(), [])


class WagtailLinksSearchBehaviorTest(WagtailPageTests):
    """End-to-end checks that the override actually changes what the search
    backend matches -- guarding against a Wagtail upgrade silently bypassing
    get_search_fields()."""

    def index_all(self):
        backend = get_search_backend()
        backend.add_bulk(Link, Link.objects.all())
        return backend

    def test_default_fields_do_not_match_name(self):
        # The zero-match behavior #34777 addresses: by default a Link is not
        # findable by its `name`.
        link = Link.objects.create(name="accountxyz", link_external="https://example.com")
        backend = self.index_all()
        self.assertNotIn(link, list(backend.autocomplete("accountxyz", Link)))

    @override_settings(WAGTAIL_LINKS_SEARCH_FIELDS=[index.SearchField("name")])
    def test_override_reaches_backend_search(self):
        link = Link.objects.create(name="accountxyz", link_external="https://example.com")
        backend = self.index_all()
        self.assertIn(link, list(backend.search("accountxyz", Link)))

    @override_settings(WAGTAIL_LINKS_SEARCH_FIELDS=[index.AutocompleteField("name")])
    def test_override_reaches_chooser_autocomplete(self):
        link = Link.objects.create(name="accountxyz", link_external="https://example.com")
        backend = self.index_all()
        self.assertIn(link, list(backend.autocomplete("account", Link)))

    @override_settings(WAGTAIL_LINKS_SEARCH_FIELDS=[index.SearchField("search_url")])
    def test_override_matches_url_segment(self):
        # search_url splits the URL so a path segment is matchable.
        link = Link.objects.create(name="u1", link_external="https://example.com/2022/report/")
        backend = self.index_all()
        self.assertIn(link, list(backend.search("2022", Link)))

    @override_settings(WAGTAIL_LINKS_SEARCH_FIELDS=[])
    def test_empty_list_matches_nothing(self):
        Link.objects.create(name="findme", title="findme", link_external="https://example.com")
        backend = self.index_all()
        self.assertEqual(list(backend.search("findme", Link)), [])
        self.assertEqual(list(backend.autocomplete("findme", Link)), [])


class WagtailLinksTest(WagtailPageTests):
    def test_get_link(self):
        link = Link.objects.create(link_external="https://example.com")
        self.assertEqual(link.url, "https://example.com")

        link = Link.objects.create(link_relative="/example.com")
        self.assertEqual(link.url, "/example.com")

        page = Page.objects.first()
        link = Link.objects.create(link_page=page)
        self.assertEqual(link.url, "")

        link = Link.objects.create(django_view_name="admin:index")
        self.assertEqual(link.url, "/admin/")

    def test_link_validation(self):
        link = Link(
            link_external="https://example.com",
            link_relative="/foo",
        )
        with self.assertRaises(ValidationError):
            link.clean()

        link = Link()
        with self.assertRaises(ValidationError):
            link.clean()

        link = Link(django_view_name="doesnotexist")
        with self.assertRaises(ValidationError):
            link.full_clean()

    @patch("wagtail_links.resolver.logger")
    def test_log_broken_links(self, mock_logger):
        link = Link.objects.create(django_view_name="doesnotexist")
        link.url
        mock_logger.warning.assert_called_with("Unable to reverse Django URL for Link[id=%s]", link.pk)

    def test_cast_link_to_string(self):
        link = Link.objects.create(name="example", link_external="https://example.com")
        self.assertEqual(f"{link}", "Link[name=example]: https://example.com")

        link = Link.objects.create(link_external="https://example.com")
        self.assertEqual(
            f"{link}",
            "Link[link_external=https://example.com]: https://example.com",
        )

        link = Link.objects.create(link_relative="/example.com")
        self.assertEqual(f"{link}", "Link[link_relative=/example.com]: /example.com")

        page = Page.objects.first()
        link = Link.objects.create(link_page=page)
        self.assertEqual(f"{link}", "Link[link_page=Root]: No Link URL")

        link = Link.objects.create(django_view_name="admin:index")
        self.assertEqual(f"{link}", "Link[django_view_name=admin:index]: /admin/")

    def test_multiple_blank_link_names(self):
        link1 = Link.objects.create(name="", link_external="https://example.com/1")
        link2 = Link.objects.create(name="", link_external="https://example.com/2")
        self.assertEqual(link1.name, "")
        self.assertEqual(link2.name, "")

    def test_search_url_splits_separators(self):
        link = Link.objects.create(link_external="https://www.archpaper.com/2022/11/best-of/")
        self.assertEqual(link.search_url, "https www archpaper com 2022 11 best of")


class WagtailLinksTagsTest(WagtailPageTests):
    def test_get_wagtail_link(self):
        Link.objects.create(name="example", link_external="https://example.com")
        context = Context({})
        template = Template(
            """
            {% load wagtail_links %}
            {% get_wagtail_link 'example' as my_link %}
            <a href="{{ my_link.url }}">Testing</a>
            """
        )
        rendered_template = template.render(context)
        self.assertInHTML('<a href="https://example.com">Testing</a>', rendered_template)

    def test_get_wagtail_link_url(self):
        Link.objects.create(name="example", link_external="https://example.com/test2/")
        context = Context({})
        template = Template(
            """
            {% load wagtail_links %}
            <a href="{% get_wagtail_link_url 'example' %}">Testing</a>
            """
        )
        rendered_template = template.render(context)
        self.assertInHTML('<a href="https://example.com/test2/">Testing</a>', rendered_template)
