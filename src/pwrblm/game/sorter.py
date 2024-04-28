"""Create sorting function."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

    from pwrblm.game.models import Game


def create_sorting_function(sort_by: str | None) -> Callable[[Game], Any] | None:
    """Create sorting function."""
    match sort_by:
        case "time_to_beat":
            return lambda item: item.time_to_beat
        case _:
            return None
