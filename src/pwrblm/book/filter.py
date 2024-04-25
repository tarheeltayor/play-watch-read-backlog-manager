"""Define filters for books."""

from __future__ import annotations

from dataclasses import dataclass

from pwrblm.book.models import Book
from pwrblm.filters.base import Filter
from pwrblm.util import is_string_close


@dataclass
class ReadFilter(Filter[Book]):
    """Filter based on having read."""

    read: bool

    def filter(self, item: Book) -> bool:
        """Define filtering function."""
        return item.completed == self.read


@dataclass
class AuthorFilter(Filter[Book]):
    """Filter based on author."""

    author: str

    def filter(self, item: Book) -> bool:
        """Define filtering function."""
        return any(
            any(is_string_close(name.lower(), self.author.lower()) for name in author.split())
            for author in item.authors
        )


@dataclass
class TagsFilter(Filter[Book]):
    """Filter based on tag."""

    tags: list[str]

    def filter(self, item: Book) -> bool:
        """Define filtering function."""
        return any(any(is_string_close(tag.lower(), curr_tag.lower()) for curr_tag in self.tags) for tag in item.tags)


@dataclass
class SeriesFilter(Filter[Book]):
    """Filter based on series."""

    series: str

    def filter(self, item: Book) -> bool:
        """Define filtering function."""
        return is_string_close(self.series.lower(), item.series.title.lower())
