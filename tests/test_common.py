from datetime import timedelta

import pytest

from issue_tracker.common.utils import duration


@pytest.mark.parametrize(
    "time_delta,expected",
    [
        (None, "-"),
        (timedelta(seconds=0), "0s"),
        (timedelta(seconds=5), "5s"),
        (timedelta(seconds=5, milliseconds=5, microseconds=10), "5s"),
        (timedelta(minutes=4, seconds=5), "4m 5s"),
        (timedelta(minutes=4, seconds=0), "4m"),
        (timedelta(hours=1, minutes=4, seconds=0), "1h 4m"),
        (timedelta(hours=1, minutes=4, seconds=6), "1h 4m"),
        (timedelta(days=23, hours=1, minutes=4, seconds=6), "23d 1h"),
        (timedelta(days=23, hours=0, minutes=4, seconds=6), "23d 4m"),
        (timedelta(days=23, hours=0, minutes=0, seconds=6), "23d 6s"),
    ],
)
def test_utils_duration(time_delta: timedelta | None, expected: str) -> None:
    """Tests duration utility is behaving as expected."""
    total_seconds = int(time_delta.total_seconds()) if time_delta is not None else None
    assert duration(total_seconds) == expected
