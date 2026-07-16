from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.template import Context, Template
from wagtail.models import Page
from wagtail.search.backends import get_search_backend
from wagtail.test.utils import WagtailPageTests

from .models import Link


class WagtailLinksSearchBehaviorTest(WagtailPageTests):
    """End-to-end checks that every field is searchable via the backend."""

    def index_all(self):
        backend = get_search_backend()
        backend.add_bulk(Link, Link.objects.all())
        return backend

    def make_page(self, title, slug):
        home = Page.objects.get(slug="home")
        page = Page(title=title, slug=slug)
        home.add_child(instance=page)
        return page

    def test_name_is_searchable(self):
        link = Link.objects.create(name="accountxyz", link_external="https://example.com")
        backend = self.index_all()
        self.assertIn(link, list(backend.search("accountxyz", Link)))
        self.assertIn(link, list(backend.autocomplete("account", Link)))

    def test_title_is_searchable(self):
        link = Link.objects.create(title="Homepage banner", link_external="https://example.com")
        backend = self.index_all()
        self.assertIn(link, list(backend.search("banner", Link)))

    def test_link_relative_is_searchable(self):
        link = Link.objects.create(name="rel", link_relative="/promos/summer/")
        backend = self.index_all()
        self.assertIn(link, list(backend.search("summer", Link)))

    def test_django_view_name_is_searchable(self):
        link = Link.objects.create(name="dv", django_view_name="admin:index")
        backend = self.index_all()
        self.assertIn(link, list(backend.search("admin:index", Link)))
        self.assertIn(link, list(backend.autocomplete("admin", Link)))

    def test_linked_page_title_is_searchable(self):
        page = self.make_page(title="Quarterly Foobar Report", slug="qfr")
        link = Link.objects.create(name="pl", link_page=page)
        backend = self.index_all()
        self.assertIn(link, list(backend.search("Foobar", Link)))

    def test_url_segment_is_searchable(self):
        # Isolate search_url's contribution: a page link's resolved URL lives in
        # no stored column, so a match on a path segment can only come from
        # search_url tokenizing the resolved URL.
        page = self.make_page(title="Untokenized", slug="zephyrsegment")
        link = Link.objects.create(name="u1", link_page=page)
        self.assertIn("zephyrsegment", link.search_url)
        backend = self.index_all()
        self.assertIn(link, list(backend.search("zephyrsegment", Link)))


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

    def test_search_url_decodes_percent_encoding(self):
        # Percent-encoded segments are decoded before tokenizing so they match
        # their human-readable form instead of being indexed as encoding noise.
        link = Link.objects.create(link_relative="/menu/caf%C3%A9/hello%20world/")
        self.assertEqual(link.search_url, "menu café hello world")


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
