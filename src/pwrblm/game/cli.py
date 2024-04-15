"""Create sub-CLI for managing games."""

# pylint: disable=dangerous-default-value,too-many-arguments
from __future__ import annotations

from itertools import chain  # noqa: TCH003
from typing import Annotated

import click  # noqa: TCH002
import typer
from rich import print as rich_print

from pwrblm.filters.base import AndFilter
from pwrblm.game.edit import edit as edit_game
from pwrblm.game.filter import (
    AchievementCompleteFilter,
    CompletedFilter,
    DeveloperFilter,
    GenreFilter,
    PlatformFilter,
    PlayedFilter,
    TagsFilter,
)
from pwrblm.game.models import Game, GameAchievements, Platform
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


@game_app.command(no_args_is_help=True)
def choose(
    ctx: typer.Context,
    num_runs: Annotated[int, typer.Option("--num-runs", "-n", help="Number of times to pick a random item")] = 50,
    platform: Annotated[
        str | None,
        typer.Option(
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
    filter_ = AndFilter[Game]()
    if platform is not None:
        filter_.add(PlatformFilter(platform))
    filter_.add(CompletedFilter(completed=completed))
    filter_.add(PlayedFilter(played=played))
    filter_.add(AchievementCompleteFilter(achievements_complete=achievements_complete))
    if tag:
        filter_.add(TagsFilter(tag))
    if genre:
        filter_.add(GenreFilter(genre))
    if developer:
        filter_.add(DeveloperFilter(developer))
    result = Picker(num_runs, filter_).pick(ctx.obj.games)
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
    edit_game(ctx, name, Platform(platform) if platform else None)
