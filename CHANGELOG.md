# Changelog

## r2.8.0

- Add support for Wagtail 6 and 6.1.

## r2.7.0

- Add support for Wagtail 5.2.
- Migrate dependency management to Poetry.

## r2.6.0

- Add support for Wagtail 5.1.

## r2.5.0

- Add Wagtail 4.0.x, 4.1.x, 4.2.x, and 5.0.x to test suite.

## r2.4.4

- Add Wagtail 3.0 to test suite.

## r2.4.3

- Use `title`, not `name` for search.

## r2.4.2

- Fix bug with search index

## r2.4.1

- Fix bug with optional `name` field
- Fix type of `title` field

## r2.4.0

- Adding optional `title` field to Links, make `name` field optional

## r2.3.0

- Made Links searchable by partial "link_page.title"

## r2.2.0

- Made Links searchable by "link_page.title"

## r2.1.0

- Added new "name" field to Link objects. Serves as a unique Link identifier.
- Added new template tags to fetch Link objects and URLs using the Link name.
- Added Django 2.2 to tox testing suite


## r2.0.0

- Updated to Wagtail 2.x. For Wagtail 1.x use version 1.0.2.


## r1.0.2

- Fix Error when Link to a String
