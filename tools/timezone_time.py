from __future__ import annotations

import datetime
import pytz
from smolagents import tool


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """
    Fetch current local time in a specified timezone.

    Args:
        timezone: A valid timezone string (e.g., 'America/New_York').

    Returns:
        A human-readable string with local time.
    """
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {e}"
