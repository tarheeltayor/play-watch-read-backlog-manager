"""Provide functionality for editing a book."""

import json
from typing import Any

import typer
from rich import print as rich_print

from pwrblm.book.models import Book
from pwrblm.editor import Editor
from pwrblm.util import is_string_close


class BookEditor(Editor[Book]):
    """Encapsulate editing of book."""

    description = "book"
    rich_emoji = "book"

    @classmethod
    def _find_match(cls, items: list[Book], **kwargs: Any) -> Book:  # noqa: ANN401
        """Find match."""
        title = str(cls.require(kwargs, "title"))
        try:
            return next(book for book in items if book.title == title)
        except StopIteration:
            rich_print(f":warning:  Could not find book :book:  with title={title}")

        matching_books = [book for book in items if is_string_close(book.title, title)]
        if not matching_books:
            rich_print(f":stop_sign: Could not find book with title close to {title}")
            raise typer.Abort
        rich_print("Choose a book to edit:")
        for idx, curr_book in enumerate(matching_books):
            rich_print(f"[{idx}] {curr_book}")
        try:
            choice = typer.prompt("Choice").strip()
            return matching_books[int(choice)]
        except (IndexError, TypeError, ValueError) as err:
            rich_print(f":stop_sign: Invalid choice {choice}")
            raise typer.Abort from err

    @classmethod
    def _extract_edited(cls, contents: bytes) -> Book:
        """Extract edited contents into book."""
        return Book.from_json(json.loads(contents))
