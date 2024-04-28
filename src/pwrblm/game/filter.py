"""Define filters."""

# pylint: disable=too-many-arguments
from __future__ import annotations

from dataclasses import dataclass

from pwrblm.filters.base import AndFilter, Filter
from pwrblm.game.models import Game
from pwrblm.util import is_string_close


def create_filter(  # noqa: PLR0913
    *,
    platform: str | None,
    completed: bool,
    played: bool,
    achievements_complete: bool,
    tag: list[str],
    genre: str,
    developer: str,
) -> Filter[Game]:
    """Create final filter."""
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
    return filter_


@dataclass
class PlatformFilter(Filter[Game]):
    """Filter based on platform."""

    platform: str

    def filter(self, item: Game) -> bool:
        """Define filtering function."""
        if self.platform == "ps":
            return item.platform.is_playstation()
        return self.platform == item.platform.value


@dataclass
class CompletedFilter(Filter[Game]):
    """Filter based on completion status."""

    completed: bool

    def filter(self, item: Game) -> bool:
        """Define filtering function."""
        return item.completed == self.completed


@dataclass
class PlayedFilter(Filter[Game]):
    """Filter based on play status."""

    played: bool

    def filter(self, item: Game) -> bool:
        """Define filtering function."""
        return item.played == self.played


@dataclass
class AchievementCompleteFilter(Filter[Game]):
    """Filter based on achievement completion."""

    achievements_complete: bool

    def filter(self, item: Game) -> bool:
        """Define filtering function."""
        return item.achievements.complete == self.achievements_complete


@dataclass
class TagsFilter(Filter[Game]):
    """Filter based on tags."""

    tags: list[str]

    def filter(self, item: Game) -> bool:
        """Define filtering function."""
        return all(any(is_string_close(game_tag, curr_tag) for game_tag in item.tags) for curr_tag in self.tags)


@dataclass
class GenreFilter(Filter[Game]):
    """Filter based on genre."""

    genre: str

    def filter(self, item: Game) -> bool:
        """Define filtering function."""
        return any(is_string_close(genre, self.genre) for genre in item.genres)


@dataclass
class DeveloperFilter(Filter[Game]):
    """Filter based on developer."""

    developer: str

    def filter(self, item: Game) -> bool:
        """Define filtering function."""
        return is_string_close(self.developer, item.developer)
