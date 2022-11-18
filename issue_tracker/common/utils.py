"""
Common utils.
"""


def duration(total_seconds: int | None) -> str:
    """
    Returns string representation of duration in seconds.
    """
    if total_seconds is None:
        return "-"

    days = total_seconds // (60 * 60 * 24)
    remaining_seconds_to_day = total_seconds % (60 * 60 * 24)

    hours = remaining_seconds_to_day // (60 * 60)
    remaining_seconds_to_hour = remaining_seconds_to_day % (60 * 60)

    minutes = remaining_seconds_to_hour // 60
    seconds = remaining_seconds_to_hour % 60

    # We want to include only the first 2 elements of the result array.
    # For example, instead of 1d 1h 1m 1s we show 1d 1h.
    result: list[str] = []

    if days:
        result.append(f"{int(days)}d")

    if hours:
        result.append(f"{int(hours)}h")

    if minutes:
        result.append(f"{int(minutes)}m")

    if seconds:
        result.append(f"{int(seconds)}s")

    if not result:
        return "0s"

    return " ".join(result[:2])
