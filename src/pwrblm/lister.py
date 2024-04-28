"""Encapsulate listing of items."""

from collections.abc import Callable
from typing import Any, Literal, TypeVar

from rich import print as rich_print

from pwrblm.filters.base import Filter

_T = TypeVar("_T")


def list_items(
    items: list[_T],
    rich_emoji: str,
    filter_: Filter[_T] | None = None,
    sorter: Callable[[_T], Any] | None = None,
    sort_direction: Literal["asc", "desc"] = "asc",
) -> None:
    """Display items."""
    if filter_ is not None:
        items = [item for item in items if filter_.filter(item)]
    if sorter is not None:
        items = sorted(items, key=sorter, reverse=sort_direction == "desc")
    for item in items:
        rich_print(f":{rich_emoji}:  {item}")
