"""Top-level backlog manager."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import typer
from jsonpickle import encode
from rich import print as rich_print

from .game.models import Game

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any


@dataclass
class BacklogManager:
    """Backlog manager."""

    path: Path
    games: list[Game] = field(default_factory=list)

    @classmethod
    def from_json(cls, file: Path, json_contents: dict[str, Any]) -> BacklogManager:
        """Create from JSON."""
        return cls(
            path=file,
            games=[Game.from_json(game) for game in json_contents.get("games", [])],
        )

    @classmethod
    def from_file(cls, file: Path) -> BacklogManager:
        """Create from file."""
        if not file.exists():
            if typer.confirm(f"Given file {file} does not exist. Would you like to create it?"):
                with file.open("wt", encoding="utf-8") as stream:
                    json.dump({}, stream)
            else:
                error = f"Given file {file} does not exist"
                raise ValueError(error)
        if not str(file).endswith(".json"):
            error = f"As of now, only supported file type is JSON. Got file {file}"
            raise ValueError(error)
        with file.open(encoding="utf-8") as stream:
            contents = json.load(stream)
        if not isinstance(contents, dict):
            error = f"Expected file {file} to parse into mapping. Instead got type {type(contents)}"
            raise TypeError(error)
        return cls.from_json(file, contents)

    def add_game(self, game: Game) -> None:
        """Add game to backlog."""
        if game in self.games:
            rich_print("Game has already been added to backlog")
            if typer.confirm("Overwrite details?"):
                self.games[self.games.index(game)].edit(game)
            return
        self.games.append(game)

    def write(self) -> None:
        """Write current backlog."""
        with self.path.open("wt", encoding="utf-8") as stream:
            stream.write(encode(self, unpicklable=False))
            stream.write("\n")

    def __getstate__(self) -> dict[str, Any]:
        """Get state for pickling."""
        return {key: value for key, value in self.__dict__.items() if key != "path"}
