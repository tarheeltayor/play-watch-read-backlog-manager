"""Create sub-CLI for managing games."""

# pylint: disable=dangerous-default-value,too-many-arguments
from __future__ import annotations

from itertools import chain  # noqa: TCH003
from typing import Annotated, Literal, cast

import click  # noqa: TCH002
import typer
from rich import print as rich_print

from pwrblm.game.edit import GameEditor
from pwrblm.game.filter import create_filter
from pwrblm.game.models import Game, GameAchievements, Platform
from pwrblm.game.sorter import create_sorting_function
from pwrblm.lister import list_items
from pwrblm.picker.model import Picker

game_app = typer.Typer(no_args_is_help=True)


@game_app.command(no_args_is_help=True)
def add(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(help="Name of game", show_default=False)],
    platform: Annotated[Platform, typer.Option(help="Platform on which to play the game", show_default=False)],
    metacritic_score: Annotated[float, typer.Option(help="Score as given on MetaCritic (out of 100)")] = 0,
    played: Annotated[
        bool,
        typer.Option("--played/--not-played", help="Whether played the game yet"),
    ] = False,
    completed: Annotated[
        bool,
        typer.Option(
            "--completed/--not-completed",
            help="Whether completed the game before",
        ),
    ] = False,
    achievements_complete: Annotated[
        bool,
        typer.Option(
            "--achievements-complete/--achievements-not-complete",
            help="Whether have completed all achievements of game",
        ),
    ] = False,
    achievements_difficulty: Annotated[float, typer.Option(help="Difficulty of completing achievements")] = 10,
    time_to_beat: Annotated[
        float,
        typer.Option(
            help="Amount of time in hours it takes to complete the game "
            "(user preference whether this is completionist or main story alone)",
        ),
    ] = 0,
    tag: Annotated[
        list[str],
        typer.Option(help="Tags to associate with the game (can be passed multiple times)"),
    ] = [],
    developer: Annotated[str, typer.Option(help="Developer of the game")] = "",
    genre: Annotated[
        list[str],
        typer.Option(help="Genres associated with the game (can be passed multiple times)"),
    ] = [],
) -> None:
    """Add a game."""
    ctx.obj.add_game(
        Game(
            name=name,
            platform=platform,
            metacritic_score=metacritic_score,
            played=played,
            completed=completed,
            achievements=GameAchievements(
                complete=achievements_complete,
                difficulty=achievements_difficulty,
            ),
            time_to_beat=time_to_beat,
            tags=[item.strip() for item in tag],
            developer=developer,
            genres=[item.strip() for item in genre],
        )
    )
    ctx.obj.write()


@game_app.command()
def choose(
    ctx: typer.Context,
    num_runs: Annotated[int, typer.Option("--num-runs", "-n", help="Number of times to pick a random item")] = 50,
    platform: Annotated[
        str | None,
        typer.Option(
            "--platform",
            "-p",
            help="Platform for which to pick a game",
            click_type=click.Choice(list(chain([item.value for item in Platform], ["ps"]))),
        ),
    ] = None,
    completed: Annotated[
        bool, typer.Option("--completed", help="Whether to choose a game that has been completed before")
    ] = False,
    played: Annotated[
        bool, typer.Option("--played", help="Whether to choose a game that has been played before")
    ] = False,
    achievements_complete: Annotated[
        bool,
        typer.Option(
            "--achievements-complete",
            help="Whether to choose a game that has had all the achievements already completed",
        ),
    ] = False,
    tag: Annotated[
        list[str],
        typer.Option(help="Only choose a game with the given tag(s) (can be passed multiple times)"),
    ] = [],
    genre: Annotated[str, typer.Option(help="Pick a game in the given genre")] = "",
    developer: Annotated[str, typer.Option(help="Pick a game from the given developer")] = "",
) -> None:
    """Pick a game."""
    result = Picker(
        num_runs,
        create_filter(
            platform=platform,
            completed=completed,
            played=played,
            achievements_complete=achievements_complete,
            tag=tag,
            genre=genre,
            developer=developer,
        ),
    ).pick(ctx.obj.games)
    rich_print(f":video_game:  {result} :video_game:")


@game_app.command(no_args_is_help=True)
def edit(
    ctx: typer.Context,
    name: Annotated[str, typer.Option(help="Name of game", show_default=False)],
    platform: Annotated[
        str | None,
        typer.Option(
            help="Platform on which to play the game",
            click_type=click.Choice([item.value for item in Platform]),
        ),
    ] = None,
) -> None:
    """Edit a game."""
    GameEditor.edit(ctx.obj.games, callback=ctx.obj.write, name=name, platform=Platform(platform) if platform else None)


@game_app.command()
def show(
    ctx: typer.Context,
    sort_by: Annotated[
        str | None, typer.Option(help="Value to sort list by", click_type=click.Choice(["time_to_beat"]))
    ] = None,
    sort_direction: Annotated[
        str, typer.Option(help="Direction in which to sort", click_type=click.Choice(["asc", "desc"]))
    ] = "asc",
    platform: Annotated[
        str | None,
        typer.Option(
            "--platform",
            "-p",
            help="Platform for which to filter games",
            click_type=click.Choice(list(chain([item.value for item in Platform], ["ps"]))),
        ),
    ] = None,
    completed: Annotated[
        bool, typer.Option("--completed", help="Whether to list games that have been completed before")
    ] = False,
    played: Annotated[
        bool, typer.Option("--played", help="Whether to list games that have been played before")
    ] = False,
    achievements_complete: Annotated[
        bool,
        typer.Option(
            "--achievements-complete",
            help="Whether to list games that have had all the achievements already completed",
        ),
    ] = False,
    tag: Annotated[
        list[str],
        typer.Option(help="Only list games with the given tag(s) (can be passed multiple times)"),
    ] = [],
    genre: Annotated[str, typer.Option(help="List games in the given genre")] = "",
    developer: Annotated[str, typer.Option(help="List games from the given developer")] = "",
) -> None:
    """Show games matching given conditions."""
    list_items(
        ctx.obj.games,
        "video_game",
        filter_=create_filter(
            platform=platform,
            completed=completed,
            played=played,
            achievements_complete=achievements_complete,
            tag=tag,
            genre=genre,
            developer=developer,
        ),
        sorter=create_sorting_function(sort_by),
        sort_direction=cast(Literal["asc", "desc"], sort_direction),
    )
