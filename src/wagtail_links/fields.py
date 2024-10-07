from collections.abc import Sequence
from typing import Any, Optional

from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields import SlugField


class NullSlugField(SlugField):  # type:ignore[type-arg]
    """
    SlugField that stores '' as None and returns None as ''

    Useful when using unique=True and forms. Implies null==blank==True.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not kwargs.get("null", True) or not kwargs.get("blank", True):
            raise ImproperlyConfigured("NullCharField implies null==blank==True")
        kwargs["null"] = kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def from_db_value(
        self,
        value: Optional[str],
        *args: Any,
        **kwargs: Any,
    ) -> Optional[str]:
        value = self.to_python(value)
        # If the value was stored as null, return empty string instead
        return value if value is not None else ""

    def get_prep_value(self, value: Optional[str]) -> Optional[str]:
        prepped = super().get_prep_value(value)
        # If the value was stored as empty string, return None instead
        return prepped if prepped != "" else None

    def deconstruct(self) -> tuple[str, str, Sequence[Any], dict[str, Any]]:
        name, path, args, kwargs = super().deconstruct()
        del kwargs["null"]
        del kwargs["blank"]
        return name, path, args, kwargs
