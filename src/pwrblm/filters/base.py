"""Create base filter."""

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Filter(Generic[T]):
    """Base class for filters."""

    @abstractmethod
    def filter(self, item: T) -> bool:
        """Filter item."""
        error = "Should be implemented in subclasses"
        raise NotImplementedError(error)


@dataclass
class AndFilter(Filter[T]):
    """Collect filters."""

    filters: list[Filter[T]] = field(default_factory=list)

    def filter(self, item: T) -> bool:
        """Fitler item."""
        return all(func.filter(item) for func in self.filters)

    def add(self, filter_: Filter[T]) -> None:
        """Add a filter."""
        self.filters.append(filter_)
