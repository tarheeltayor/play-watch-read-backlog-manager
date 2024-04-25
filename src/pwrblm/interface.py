"""Define interface for backlog models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from jsonpickle import encode

if TYPE_CHECKING:
    from typing_extensions import Self


class BacklogModelMixIn:
    """Define common interface for backlog model."""

    def edit(self, other: Self) -> None:
        """Edit by overwriting attributes."""
        for key, value in other.__dict__.items():
            setattr(self, key, value)

    def encode(self, indent: int | None = None) -> str:
        """Encode object as JSON."""
        return str(encode(self, unpicklable=False, indent=indent))
