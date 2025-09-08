# commands/cmd_fastfetch.py
import platform
import re
import datetime
from pathlib import Path

# Try to import psutil for uptime, provide a fallback if not available
try:
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False

# In a real terminal, colorama would handle ANSI escape codes.
# For direct output in a web environment, these colors might not render
# unless the terminal emulator supports them.
# We'll include them as they would be in a real terminal script.
class Fore:
    BLACK = '\x1b[30m'
    RED = '\x1b[31m'
    GREEN = '\x1b[32m'
    YELLOW = '\x1b[33m'
    BLUE = '\x1b[34m'
    MAGENTA = '\x1b[35m'
    CYAN = '\x1b[36m'
    WHITE = '\x1b[37m'
    RESET = '\x1b[39m'

class Style:
    BRIGHT = '\x1b[1m'
    DIM = '\x1b[2m'
    NORMAL = '\x1b[22m'
    RESET_ALL = '\x1b[0m'

def strip_ansi(text):
    """Removes ANSI escape codes from a string."""
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

class FastfetchCommand:
    def _get_uptime(self):
        """Calculates and returns the system uptime in a human-readable format."""
        if not _PSUTIL_AVAILABLE:
            return "N/A (psutil not installed)"
        try:
            boot_time_timestamp = psutil.boot_time()
            boot_datetime = datetime.datetime.fromtimestamp(boot_time_timestamp)
            current_datetime = datetime.datetime.now()
            uptime_seconds = (current_datetime - boot_datetime).total_seconds()

            days = int(uptime_seconds // (24 * 3600))
            uptime_seconds %= (24 * 3600)
            hours = int(uptime_seconds // 3600)
            uptime_seconds %= 3600
            minutes = int(uptime_seconds // 60)
            seconds = int(uptime_seconds % 60)

            uptime_str = []
            if days > 0:
                uptime_str.append(f"{days}d")
            if hours > 0:
                uptime_str.append(f"{hours}h")
            if minutes > 0:
                uptime_str.append(f"{minutes}m")
            if seconds > 0 or not uptime_str: # Ensure seconds are shown if nothing else, or if uptime is very short
                 uptime_str.append(f"{seconds}s")

            return " ".join(uptime_str)
        except Exception:
            return "Error calculating uptime"


    def run(self):
        # Load m5rcode version
        m5rcode_version = "1.0.0"
        try:
            version_file = Path(__file__).parents[1] / "version.txt"
            if version_file.exists():
                m5rcode_version = version_file.read_text().strip()
        except Exception:
            pass # Keep default "1.0.0" if file not found or error

        # ASCII "M" logo (22 lines)
        # Ensure consistent width for ASCII art (27 characters wide including leading/trailing spaces)
        ascii_m = [
            "           _____           ", # 27 chars
            "          /\\   \\          ", # 27 chars
            "         /::\\____\\         ", # 27 chars
            "        /::::|   |         ", # 27 chars
            "       /:::::|   |         ", # 27 chars
            "      /::::::|   |         ", # 27 chars
            "     /:::/|::|   |         ", # 27 chars
            "    /:::/ |::|   |         ", # 27 chars
            "   /:::/  |::|___|______   ", # 27 chars
            "  /:::/   |::::::::\\   \\  ", # 27 chars
            " /:::/    |:::::::::\\____\\", # 27 chars
            " \\::/    / ~~~~~/:::/   / ", # 27 chars
            "  \\/____/      /:::/   /  ", # 27 chars
            "              /:::/   /   ", # 27 chars
            "             /:::/   /    ", # 27 chars
            "            /:::/   /     ", # 27 chars
            "           /:::/   /      ", # 27 chars
            "          /:::/   /       ", # 27 chars
            "         /:::/   /        ", # 27 chars
            "         \\::/   /         ", # 27 chars
            "          \\/____/          ", # 27 chars
            "                           ", # 27 chars (padding line)
        ]

        # Get uptime
        uptime_info = self._get_uptime()

        # Labels for system info, padded to a fixed width for alignment
        # Maximum label length is "m5rcode Version:" (15 chars)
        LABEL_PAD = 17 # Consistent padding for labels

        # System info lines
        actual_info_lines = [
            f"{Fore.CYAN}{'m5rcode Version:':<{LABEL_PAD}}{Fore.RESET} {m5rcode_version}",
            f"{Fore.CYAN}{'Python Version:':<{LABEL_PAD}}{Fore.RESET} {platform.python_version()}",
            f"{Fore.CYAN}{'Platform:':<{LABEL_PAD}}{Fore.RESET} {platform.system() + ' ' + platform.release()}",
            f"{Fore.CYAN}{'Machine:':<{LABEL_PAD}}{Fore.RESET} {platform.machine()}",
            f"{Fore.CYAN}{'Processor:':<{LABEL_PAD}}{Fore.RESET} {platform.processor()}",
            f"{Fore.CYAN}{'Uptime:':<{LABEL_PAD}}{Fore.RESET} {uptime_info}",
        ]

        # Determine the widest string in actual_info_lines after stripping ANSI for content length
        max_info_content_width = 0
        for line in actual_info_lines:
            max_info_content_width = max(max_info_content_width, len(strip_ansi(line)))

        # Determine the fixed width for ASCII art after stripping
        ascii_art_display_width = len(strip_ansi(ascii_m[0])) # Assuming all ASCII lines have same display width

        # Define a consistent separator width between ASCII art and info lines
        SEPARATOR_WIDTH = 4 # e.g., "    "

        # Calculate padding for vertical centering
        num_ascii_lines = len(ascii_m)
        num_info_content_lines = len(actual_info_lines)

        total_blank_lines_info = num_ascii_lines - num_info_content_lines
        top_padding_info = total_blank_lines_info // 2
        bottom_padding_info = total_blank_lines_info - top_padding_info

        info_lines_padded = [""] * top_padding_info + actual_info_lines + [""] * bottom_padding_info

        # Pad info_lines_padded to match ascii_m's length if there's any discrepancy
        # This shouldn't be necessary if num_ascii_lines calculation is correct above
        # but as a safeguard:
        max_overall_lines = max(num_ascii_lines, len(info_lines_padded))
        ascii_m += [""] * (max_overall_lines - len(ascii_m))
        info_lines_padded += [""] * (max_overall_lines - len(info_lines_padded))


        # Calculate the overall box width
        # The widest possible line will be (ASCII art width) + (Separator width) + (Max info content width)
        box_content_width = ascii_art_display_width + SEPARATOR_WIDTH + max_info_content_width

        # Add buffer for box borders and internal padding
        box_width = box_content_width + 2 # For left and right borders

        # Ensure minimum width for header title
        min_header_width = len("m5rcode Fastfetch") + 4 # Title + padding
        box_width = max(box_width, min_header_width)


        # Header of the box
        print(Fore.MAGENTA + "╭" + "─" * (box_width - 2) + "╮")
        title = "m5rcode Fastfetch"
        padded_title = title.center(box_width - 2)
        print(Fore.MAGENTA + "│" + Fore.CYAN + padded_title + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + "├" + "─" * (box_width - 2) + "┤")

        # Body of the box
        for ascii_line, info_line in zip(ascii_m, info_lines_padded):
            effective_ascii_width = len(strip_ansi(ascii_line))
            effective_info_width = len(strip_ansi(info_line))

            # Calculate the current line's effective content width
            current_line_content_width = effective_ascii_width + SEPARATOR_WIDTH + effective_info_width

            # Calculate padding needed to fill the box width for THIS specific line
            padding_needed = (box_width - 2) - current_line_content_width
            padding_needed = max(0, padding_needed) # Ensure non-negative

            print(
                Fore.MAGENTA + "│" +
                ascii_line +
                " " * SEPARATOR_WIDTH +
                info_line +
                " " * padding_needed +
                Fore.MAGENTA + "│"
            )

        # Footer of the box
        print(Fore.MAGENTA + "╰" + "─" * (box_width - 2) + "╯" + Style.RESET_ALL)

# Example usage (for testing this script directly)
if __name__ == "__main__":
    # If psutil is not installed, the uptime will show "N/A (psutil not installed)"
    # To test full functionality, run `pip install psutil` in your environment.
    FastfetchCommand().run()
