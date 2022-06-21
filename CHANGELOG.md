# Changelog

## v2.4.4

- Add Wagtail 3.0 to test suite.

## v2.4.3

- Use `title`, not `name` for search.

## v2.4.2

- Fix bug with search index

## v2.4.1

- Fix bug with optional `name` field
- Fix type of `title` field

## v2.4.0

- Adding optional `title` field to Links, make `name` field optional

## v2.3.0

- Made Links searchable by partial "link_page.title"

## v2.2.0

- Made Links searchable by "link_page.title"

## v2.1.0

- Added new "name" field to Link objects. Serves as a unique Link identifier.
- Added new template tags to fetch Link objects and URLs using the Link name.
- Added Django 2.2 to tox testing suite


## v2.0.0

- Updated to Wagtail 2.x. For Wagtail 1.x use version 1.0.2.


## v1.0.2

- Fix Error when Link to a String
