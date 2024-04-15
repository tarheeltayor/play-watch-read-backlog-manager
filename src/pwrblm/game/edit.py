"""Provide functionality for editing a game."""

import json
from os import environ
from subprocess import call
from tempfile import NamedTemporaryFile
from typing import Final

import typer
from rich import print as rich_print

from pwrblm.game.models import Game, Platform
from pwrblm.util import is_string_close

ALLOWED_EDITORS: Final = ("usr/bin/vim", "vim")


def edit(ctx: typer.Context, name: str, platform: Platform | None) -> None:
    """Edit a game."""
    editor = environ.get("EDITOR", "vim")
    if editor.strip() not in ALLOWED_EDITORS:
        error = f"Unsupported editor {editor}"
        raise ValueError(error)
    game = __find_game(ctx.obj.games, name, platform)
    with NamedTemporaryFile() as temp_file:
        temp_file.write(game.encode(indent=4).encode("utf-8"))
        temp_file.flush()

        call([editor, temp_file.name])  # noqa: S603

        temp_file.seek(0)
        edited = __extract_edited_game(temp_file.read())
    game.edit(edited)

    ctx.obj.write()

    rich_print(f"Saved new details :video_game:  {game}")


def __find_game(games: list[Game], name: str, platform: Platform | None) -> Game:
    """Find game given information."""
    try:
        return next(game for game in games if game.name == name and (game.platform == platform if platform else True))
    except StopIteration:
        rich_print(
            f":warning:  Could not find game :video_game:  with name={name} "
            f"and platform={platform if platform else 'ANY'}"
        )

    matching_games = [
        game for game in games if (game.platform == platform if platform else True) and is_string_close(game.name, name)
    ]
    if not matching_games:
        rich_print(
            f":stop_sign: Could not find game with platform={platform if platform else 'ANY'} and name close to {name}"
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


def __extract_edited_game(contents: bytes) -> Game:
    try:
        return Game.from_json(json.loads(contents))
    except json.decoder.JSONDecodeError as err:
        rich_print(f":stop_sign: Failed to decode edited game {contents!r} as JSON")
        raise typer.Abort from err
    except (KeyError, TypeError, ValueError) as err:
        rich_print(f":stop_sign: Failed to parse edited game {contents!r} into game - {type(err)}: {err}")
        raise typer.Abort from err
