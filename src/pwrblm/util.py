"""Define utility functions."""

from difflib import SequenceMatcher
from typing import Final

MIN_DIFF: Final = 0.6
MIN_CLOSE_SIZE: Final = 5


def is_string_close(one: str, two: str) -> bool:
    """Determine if strings are 'close enough'."""
    seq = SequenceMatcher(lambda item: item.isspace(), one.lower(), two.lower())
    return seq.ratio() >= MIN_DIFF or seq.find_longest_match().size >= MIN_CLOSE_SIZE
