from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def reindex_links(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    """Re-index existing Links so the expanded ``search_fields`` take effect.

    Making every field searchable only changes what gets written to the search
    index going forward; links already stored downstream stay indexed under the
    old field set until re-indexed. Doing it here means projects pulling in this
    version pick up the new searchable fields on ``migrate`` without having to
    run ``update_index`` by hand.
    """
    from wagtail.search.backends import get_search_backends

    # The concrete model (not the historical one) carries ``search_fields``.
    from wagtail_links.models import Link

    for backend in get_search_backends():
        # Backends like the "dummy" test backend have no rebuilder and nothing
        # to index into.
        if not getattr(backend, "rebuilder_class", None):
            continue
        backend.add_bulk(Link, Link.objects.all())


class Migration(migrations.Migration):
    dependencies = [
        ("wagtail_links", "0007_auto_20200101_1658"),
    ]

    operations = [
        migrations.RunPython(reindex_links, migrations.RunPython.noop),
    ]
