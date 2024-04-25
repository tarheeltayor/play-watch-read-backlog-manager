"""Create sub-CLI for managing books."""

# pylint: disable=dangerous-default-value,too-many-arguments
from __future__ import annotations

from typing import Annotated

import typer
from rich import print as rich_print

from pwrblm.book.edit import BookEditor
from pwrblm.book.filter import AuthorFilter, ReadFilter, SeriesFilter, TagsFilter
from pwrblm.book.models import Book, Series
from pwrblm.filters.base import AndFilter
from pwrblm.picker.model import Picker

book_app = typer.Typer(no_args_is_help=True)


@book_app.command(no_args_is_help=True)
def add(
    ctx: typer.Context,
    title: Annotated[str, typer.Option(help="Title of book", show_default=False)],
    pages: Annotated[int, typer.Option(help="Number of pages in book")] = 0,
    started: Annotated[bool, typer.Option("--started/--not-started", help="Whether started the book")] = False,
    completed: Annotated[
        bool, typer.Option("--completed/--not-completed", help="Whether have completed the book")
    ] = False,
    author: Annotated[list[str], typer.Option(help="Author(s) who wrote the book (can be passed multiple times)")] = [],
    genre: Annotated[
        list[str], typer.Option(help="Genres associated with the book (can be passed multiple times)")
    ] = [],
    tag: Annotated[list[str], typer.Option(help="Tags to associate with the book (can be passed multiple times)")] = [],
    series_title: Annotated[str, typer.Option(help="Title of the book's associated series")] = "",
    series_index: Annotated[int, typer.Option(help="Index in the associated series for the given book")] = 0,
) -> None:
    """Add a book to the backlog."""
    ctx.obj.add_book(
        Book(
            title=title,
            pages=pages,
            started=started,
            completed=completed,
            authors=[item.strip() for item in author],
            genres=[item.strip() for item in genre],
            tags=[item.strip() for item in tag],
            series=Series(
                title=series_title,
                index=series_index,
            ),
        )
    )
    ctx.obj.write()


@book_app.command()
def choose(
    ctx: typer.Context,
    num_runs: Annotated[int, typer.Option("--num-runs", "-n", help="Number of times to pick a random item")] = 50,
    read: Annotated[
        bool, typer.Option("--read/--not-read", help="Whether to choose a book which has been read before")
    ] = False,
    author: Annotated[str, typer.Option(help="Only choose a book with the given author")] = "",
    tag: Annotated[
        list[str], typer.Option(help="Only choose a book with the given tag(s) (can be passed multiple times)")
    ] = [],
    series: Annotated[str, typer.Option(help="Only choose a book in the given series")] = "",
) -> None:
    """Pick a book."""
    filter_ = AndFilter[Book]()
    filter_.add(ReadFilter(read))
    if author:
        filter_.add(AuthorFilter(author))
    if tag:
        filter_.add(TagsFilter(tag))
    if series:
        filter_.add(SeriesFilter(series))
    result = Picker(num_runs, filter_).pick(ctx.obj.books)
    rich_print(f":book:  {result} :book:")


@book_app.command(no_args_is_help=True)
def edit(
    ctx: typer.Context,
    title: Annotated[str, typer.Option(help="Title of book", show_default=False)],
) -> None:
    """Edit a book."""
    BookEditor.edit(ctx.obj.books, callback=ctx.obj.write, title=title)
