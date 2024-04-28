"""Create base filter."""

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar

_T = TypeVar("_T")


@dataclass
class Filter(Generic[_T]):
    """Base class for filters."""

    @abstractmethod
    def filter(self, item: _T) -> bool:
        """Filter item."""
        error = "Should be implemented in subclasses"
        raise NotImplementedError(error)


@dataclass
class AndFilter(Filter[_T]):
    """Collect filters."""

    filters: list[Filter[_T]] = field(default_factory=list)

    def filter(self, item: _T) -> bool:
        """Fitler item."""
        return all(func.filter(item) for func in self.filters)

    def add(self, filter_: Filter[_T]) -> None:
        """Add a filter."""
        self.filters.append(filter_)
