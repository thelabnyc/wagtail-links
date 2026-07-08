from django import forms

from .models import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = [
            "title",
            "name",
            "link_external",
            "link_relative",
            "link_page",
            "django_view_name",
        ]
