"""Represent a game."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, unique
from pathlib import Path
from typing import Any

from jsonpickle import encode
from jsonschema import Draft202012Validator
from yaml import safe_load

with Path(__file__).parent.parent.joinpath("resources", "schema", "game.schema.yaml").resolve().open(
    encoding="utf-8"
) as stream:
    GAMES_SCHEMA = Draft202012Validator(safe_load(stream))


@unique
class Platform(Enum):
    """Platform on which to play games."""

    PS5 = "ps5"
    PS4 = "ps4"
    PS3 = "ps3"
    SWITCH = "switch"
    PC = "pc"

    def is_playstation(self) -> bool:
        """Determine whether platform is a PlayStation type."""
        return "ps" in self.value

    def __str__(self) -> str:
        """Represent as string."""
        return self.value

    def __repr__(self) -> str:
        """Get official representation as string."""
        return str(self)


@dataclass
class GameAchievements:
    """Represent achievements of a game."""

    complete: bool = False
    difficulty: float = 10

    @classmethod
    def from_json(cls, json_rep: dict[str, Any]) -> GameAchievements:
        """Create from JSON."""
        return cls(
            complete=json_rep.get("complete", False),
            difficulty=json_rep.get("difficulty", 10),
        )


@dataclass
class Game:
    """Encapsulate a game."""

    # pylint: disable=too-many-instance-attributes
    name: str
    platform: Platform
    metacritic_score: float = 0.0
    played: bool = False
    completed: bool = False
    achievements: GameAchievements = field(default_factory=GameAchievements)
    time_to_beat: float = 0.0
    tags: list[str] = field(default_factory=list)
    developer: str = ""
    genres: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Perform post-intialization validation."""
        GAMES_SCHEMA.validate(json.loads(self.encode()))

    def edit(self, other_game: Game) -> None:
        """Edit game by overwriting attributes."""
        for key, value in other_game.__dict__.items():
            setattr(self, key, value)

    @classmethod
    def from_json(cls, json_rep: dict[str, Any]) -> Game:
        """Create from JSON."""
        GAMES_SCHEMA.validate(json_rep)
        return cls(
            name=json_rep["name"],
            platform=Platform(json_rep["platform"]),
            metacritic_score=json_rep.get("metacritic_score", 0.0),
            played=json_rep.get("played", False),
            completed=json_rep.get("completed", False),
            achievements=GameAchievements.from_json(json_rep.get("achievements", {})),
            time_to_beat=json_rep.get("time_to_beat", 0.0),
            tags=json_rep.get("tags", []),
            developer=json_rep.get("developer", ""),
            genres=json_rep.get("genres", []),
        )

    def encode(self, indent: int | None = None) -> str:
        """Encode object as JSON."""
        return str(encode(self, unpicklable=False, indent=indent))

    def __hash__(self) -> int:
        """Hash an object."""
        return hash((self.name, self.platform.value))

    def __getstate__(self) -> dict[str, Any]:
        """Get state for pickling."""
        return {key: value.value if isinstance(value, Enum) else value for key, value in self.__dict__.items()}
