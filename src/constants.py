"""File that contains all the constants for the other files.
"""

INDEXES = "\s*,\s*"
RANGE_DELIMITER = "-"
RANGE_COMPONENTS = f"\s*{RANGE_DELIMITER}\s*"

info = {
        "channels" : (),
        "videos": ("id", "title", "viewCo")
    }
clear_commands = {
    "darwin": "clear",
    "linux": "clear",
    "win32": "cls",
}
