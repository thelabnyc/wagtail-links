# wagtail-links

## Purpose

Wagtail links has two goals:

- Provide a consistent way to refer to links, which may be of different types, so as to reduce decision fatigue
- Minimize broken links as much as possible.



## Install

Install wagtail-links via Pip.

```sh
pip install wagtail-links
```

Add `wagtail_links` to your Django project's `INSTALLED_APPS` setting.

Run database migrations.

```sh
python manage.py migrate
```


## Usage

Add a foreign key to the page you wish to add links to.

```py
my_link = models.ForeignKey(
    'wagtail_links.Link',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='+'
)
```

Neat:

![](admin.png)

You may use it like:

```html
<a href="{{ self.link.url }}">Link here</a>
```

From a template, you can also load a link by its name:

```html
{% load get_wagtail_link_url from wagtail_links %}

<a href="{% get_wagtail_link_url 'my-link' %}">Link here</a>
```

This is useful for global page links, navigation, etc.


## Customising searchable fields

By default, link search (in the Snippets area and in link choosers) matches the
link's `title` and its linked page's title. To override which fields are
searchable, set `WAGTAIL_LINKS_SEARCH_FIELDS` to a list of
`wagtail.search.index` fields:

```py
# settings.py
from wagtail.search import index

WAGTAIL_LINKS_SEARCH_FIELDS = [
    index.AutocompleteField("title"),
    index.AutocompleteField("name"),
    index.AutocompleteField("link_external"),
    index.AutocompleteField("link_relative"),
]
```

This **replaces** the default entirely, so list every field you want
searchable — for example, re-add
`index.RelatedFields("link_page", [index.AutocompleteField("title")])` to keep
matching the linked page's title. Use `index.SearchField(field, boost=N)` to
rank some fields above others in full-text search; `index.AutocompleteField`
powers the type-ahead matching used in the link choosers.

The `Link` model also exposes a `search_url` property: the resolved URL with
separators replaced by spaces. Index it so full-text backends can match
individual host/path segments (e.g. `2022` in `.../2022/...`), which they
can't do against a raw URL (Postgres indexes it as one opaque token):

```py
WAGTAIL_LINKS_SEARCH_FIELDS = [
    index.SearchField("title", boost=10),
    index.AutocompleteField("title"),
    index.SearchField("search_url"),
    index.AutocompleteField("search_url"),
]
```

Leaving it unset keeps the default. After changing it, run
`python manage.py update_index` to re-index existing links.


## Validation and logging

The Link model will validate that one and only one field is set.
It will also disallow invalid Django reverse view names.

If a URL cannot be determined, we'll log the issue as a warning. We won't throw an exception as that would be bad for users. You are responsible for capturing this log warning, perhaps using Sentry.

For example - let's say you make a Django view name called admin:index. This would typically give you `/admin/`. Later the admin application is removed from the program, now this link fails. It will now display "" and generate a warning in your server logs.
