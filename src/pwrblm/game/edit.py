"""Provide functionality for editing a game."""

import json
from typing import Any, cast

import typer
from rich import print as rich_print

from pwrblm.editor import Editor
from pwrblm.game.models import Game, Platform
from pwrblm.util import is_string_close


class GameEditor(Editor[Game]):
    """Encapsulate editing of game."""

    description = "game"
    rich_emoji = "video_game"

    @classmethod
    def _find_match(cls, items: list[Game], **kwargs: Any) -> Game:  # noqa: ANN401
        """Find match."""
        name = str(cls.require(kwargs, "name"))
        platform = cast(Platform | None, kwargs.get("platform"))
        try:
            return next(
                game for game in items if game.name == name and (game.platform == platform if platform else True)
            )
        except StopIteration:
            rich_print(
                f":warning:  Could not find game :video_game:  with name={name} "
                f"and platform={platform if platform else 'ANY'}"
            )

        matching_games = [
            game
            for game in items
            if (game.platform == platform if platform else True) and is_string_close(game.name, name)
        ]
        if not matching_games:
            rich_print(
                f":stop_sign: Could not find game with platform={platform if platform else 'ANY'} "
                f"and name close to {name}"
            )
            raise typer.Abort
        rich_print("Choose a game to edit:")
        for idx, curr_game in enumerate(matching_games):
            rich_print(f"[{idx}] {curr_game}")
        try:
            choice = typer.prompt("Choice").strip()
            return matching_games[int(choice)]
        except (IndexError, TypeError, ValueError) as err:
            rich_print(f":stop_sign: Invalid choice {choice}")
            raise typer.Abort from err

    @classmethod
    def _extract_edited(cls, contents: bytes) -> Game:
        """Extract edited contents into game."""
        return Game.from_json(json.loads(contents))
