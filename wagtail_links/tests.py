from django.core.exceptions import ValidationError
from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page
from unittest.mock import patch


from .models import Link


class WagtailLinksTests(WagtailPageTests):
    def test_get_link(self):
        link = Link.objects.create(link_external="https://example.com")
        self.assertEqual(str(link), "https://example.com")

        link = Link.objects.create(link_relative="/example.com")
        self.assertEqual(str(link), "/example.com")

        page = Page.objects.first()
        link = Link.objects.create(link_page=page)
        self.assertEqual(str(link), "")

        link = Link.objects.create(django_view_name="admin:index")
        self.assertEqual(str(link), "/admin/")

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

    @patch('wagtail_links.models.logger')
    def test_log_broken_links(self, mock_logger):
        link = Link.objects.create(django_view_name="doesnotexist")
        link.link
        mock_logger.warning.assert_called_with(
            "Unable to reverse django url for link id 1")
