"""Models for representing books."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from yaml import safe_load

from pwrblm.interface import BacklogModelMixIn

with Path(__file__).parent.parent.joinpath("resources", "schema", "book.schema.yaml").resolve().open(
    encoding="utf-8"
) as stream:
    BOOKS_SCHEMA = Draft202012Validator(safe_load(stream))


@dataclass
class Series:
    """Encapsulate a book's position in a series."""

    title: str = ""
    index: int = 0


@dataclass
class Book(BacklogModelMixIn):
    """Encapsulate a book."""

    # pylint: disable=too-many-instance-attributes
    title: str
    pages: int = 0
    started: bool = False
    completed: bool = False
    authors: list[str] = field(default_factory=list)
    genres: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    series: Series = field(default_factory=Series)

    def __post_init__(self) -> None:
        """Perform post-initialization validation."""
        BOOKS_SCHEMA.validate(json.loads(self.encode()))

    @classmethod
    def from_json(cls, json_rep: dict[str, Any]) -> Book:
        """Create from JSON."""
        BOOKS_SCHEMA.validate(json_rep)
        return cls(
            title=json_rep["title"],
            pages=json_rep.get("pages", 0),
            started=json_rep.get("started", False),
            completed=json_rep.get("completed", False),
            authors=json_rep.get("authors", []),
            genres=json_rep.get("genres", []),
            tags=json_rep.get("tags", []),
            series=Series(
                title=json_rep.get("series", {}).get("title", json_rep["title"]),
                index=json_rep.get("series", {}).get("index", 0),
            ),
        )

    def __hash__(self) -> int:
        """Hash an object."""
        return hash((self.title, tuple(self.authors)))

    def __getstate__(self) -> dict[str, Any]:
        """Get state for pickling."""
        return self.__dict__
