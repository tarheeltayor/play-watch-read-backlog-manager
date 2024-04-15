"""Model for picking item."""

from collections import Counter
from dataclasses import dataclass
from secrets import choice
from typing import Generic, TypeVar

from pwrblm.filters.base import Filter

T = TypeVar("T")


@dataclass
class Picker(Generic[T]):
    """Pick an item."""

    num_runs: int
    filter: Filter[T]

    def pick(self, items: list[T]) -> T:
        """Pick an item out of the list."""
        if not items:
            error = "Cannot pass an empty list to pick"
            raise ValueError(error)
        filtered = [item for item in items if self.filter.filter(item)]
        if not filtered:
            error = f"After applying filter, there were no eligible items from which to choose: filter={self.filter}"
            raise ValueError(error)
        result = self.__pick_helper(filtered)
        while len(result) != 1:
            result = self.__pick_helper(filtered)
        return result[0]

    def __pick_helper(self, items: list[T]) -> list[T]:
        result = Counter(choice(items) for _ in range(self.num_runs)).most_common()
        max_count = result[0][1]
        return [item for item, count in result if count == max_count]
