from __future__ import annotations

import shutil
from smolagents import tool


@tool
def disk_free(path: str = "/") -> str:
    """
    Show total/used/free disk space for a given filesystem path.

    Args:
        path: Filesystem path to inspect (e.g., '/', '/home/user').

    Returns:
        A human-friendly string with total/used/free sizes.
    """
    try:
        usage = shutil.disk_usage(path)  # (total, used, free) in bytes
    except Exception as e:
        return f"Error reading disk usage for path='{path}': {e}"

    def fmt_bytes(n: int) -> str:
        units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
        x = float(n)
        i = 0
        while x >= 1024.0 and i < (len(units) - 1):
            x /= 1024.0
            i += 1
        return f"{x:.2f} {units[i]}"

    total = fmt_bytes(usage.total)
    used = fmt_bytes(usage.used)
    free = fmt_bytes(usage.free)
    return f"Disk usage for '{path}': total={total}, used={used}, free={free}"
