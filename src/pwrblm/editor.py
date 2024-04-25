"""Encapsulate editing."""

import json
from collections.abc import Callable
from os import environ
from subprocess import call
from tempfile import NamedTemporaryFile
from typing import Any, ClassVar, Final, Generic, TypeVar

import typer
from rich import print as rich_print

from pwrblm.interface import BacklogModelMixIn

ALLOWED_EDITORS: Final = ("/usr/bin/vim", "vim")
SUBCLASS_IMPLEMENT: Final = "Must be implemented in subclasses"
T = TypeVar("T", bound=BacklogModelMixIn)


class Editor(Generic[T]):
    """Encapsulate editing logic."""

    description: ClassVar[str]
    rich_emoji: ClassVar[str]

    @classmethod
    def edit(cls, items: list[T], callback: Callable[[], None] = lambda: None, **kwargs: Any) -> None:  # noqa: ANN401
        """Edit."""
        editor = environ.get("EDITOR", "vim")
        if editor.strip() not in ALLOWED_EDITORS:
            error = f"Unsupported editor {editor}"
            raise ValueError(error)
        item = cls._find_match(items, **kwargs)
        with NamedTemporaryFile() as temp_file:
            temp_file.write(item.encode(indent=4).encode("utf-8"))
            temp_file.flush()

            call([editor, temp_file.name])  # noqa: S603

            temp_file.seek(0)
            edited = cls.__do_extract_edited(temp_file.read())
        item.edit(edited)
        callback()
        rich_print(f"Saved new details :{cls.rich_emoji}:  {item} :{cls.rich_emoji}:")

    @staticmethod
    def require(kwargs: dict[str, Any], key: str) -> Any:  # noqa: ANN401
        """Require a key in kwargs."""
        if key not in kwargs:
            rich_print(f"{key} not found in kwargs {kwargs}")
            raise typer.Abort
        return kwargs[key]

    @classmethod
    def _find_match(cls, items: list[T], **kwargs: Any) -> T:  # noqa: ANN401
        """Find match."""
        raise NotImplementedError(SUBCLASS_IMPLEMENT)

    @classmethod
    def _extract_edited(cls, contents: bytes) -> T:
        """Extract edited contents into model."""
        raise NotImplementedError(SUBCLASS_IMPLEMENT)

    @classmethod
    def __do_extract_edited(cls, contents: bytes) -> T:
        """Extract edited contents into model."""
        try:
            return cls._extract_edited(contents)
        except json.decoder.JSONDecodeError as err:
            rich_print(f":stop_sign: Failed to decode edited {cls.description} {contents!r} as JSON")
            raise typer.Abort from err
        except (KeyError, TypeError, ValueError) as err:
            rich_print(
                f":stop_sign: Failed to parse edited {cls.description} {contents!r} "
                f"into {cls.description} - {type(err)}: {err}"
            )
            raise typer.Abort from err
