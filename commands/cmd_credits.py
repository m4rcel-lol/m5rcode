# commands/cmd_credits.py
from colorama import Fore, Style


class CreditsCommand:
    def run(self):
        box_width = 70
        title = "Credits"

        credits = [
            (f"{Fore.CYAN}m5rcel{Fore.RESET}", "Lead Developer"),
            (f"{Fore.YELLOW}pythonjs.cfd{Fore.RESET}", "Project Hosting & Deployment"),
            (f"{Fore.MAGENTA}colorama{Fore.RESET}", "Used for terminal styling"),
            (f"{Fore.GREEN}fastfetch inspired{Fore.RESET}", "Design influence"),
            (f"{Fore.RED}openai.com{Fore.RESET}", "Some smart AI help ;)"),
        ]

        # Top border
        print(Fore.MAGENTA + "╭" + "─" * (box_width - 2) + "╮")
        print(Fore.MAGENTA + "│" + Fore.CYAN + f"{title:^{box_width - 2}}" + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + "├" + "─" * (box_width - 2) + "┤")

        # Content
        for name, role in credits:
            line = f"{name:<30} {Fore.WHITE}- {role}"
            padding = box_width - 3 - len(strip_ansi(line))
            print(Fore.MAGENTA + "│ " + line + " " * padding + Fore.MAGENTA + "│")

        # Bottom border
        print(Fore.MAGENTA + "╰" + "─" * (box_width - 2) + "╯" + Style.RESET_ALL)


def strip_ansi(text):
    import re
    return re.sub(r'\x1b\[[0-9;]*m', '', text)
