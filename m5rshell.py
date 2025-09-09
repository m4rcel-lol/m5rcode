import os
import cmd
from colorama import init, Fore, Style
from pyfiglet import Figlet
import time

# Import Discord RPC library
from pypresence import Presence, exceptions

# Import your existing command modules
from commands.cmd_new import NewCommand
from commands.cmd_nano import NanoCommand
from commands.cmd_run import RunCommand
from commands.cmd_fastfetch import FastfetchCommand
from commands.cmd_credits import CreditsCommand
from commands.cmd_cd import CdCommand
from commands.cmd_exit import ExitCommand
from commands.cmd_wdir import WdirCommand

# Initialize colorama
init(autoreset=True)

CLIENT_ID = '1414669512158220409'

class M5RShell(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.base_dir = os.path.join(os.path.expanduser("~"), "m5rcode", "files")
        os.makedirs(self.base_dir, exist_ok=True)

        self.cwd = self.base_dir
        os.chdir(self.cwd)

        self.update_prompt()

        self.rpc_active = False
        self.rpc = None
        self._connect_rpc()

        if self.rpc_active:
            self._set_idle_presence()

    # --- Discord RPC stuff ---
    def _connect_rpc(self):
        try:
            self.rpc = Presence(CLIENT_ID)
            self.rpc.connect()
            self.rpc_active = True
        except exceptions.DiscordNotFound:
            print(Fore.YELLOW + "[RPC] Discord not found. RPC disabled." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[RPC Error] {e}" + Style.RESET_ALL)

    def _set_idle_presence(self):
        if self.rpc_active and self.rpc:
            try:
                self.rpc.update(
                    details="Using the shell",
                    state="Waiting for commands...",
                    large_image="m5rcode_logo",  # big icon for all RPC updates
                    large_text="m5rcode Shell",
                    small_image="shell_icon",    # small icon for idle
                    small_text="Idle"
                )
            except Exception:
                self.rpc_active = False

    def _set_editing_presence(self, filename):
        if self.rpc_active and self.rpc:
            try:
                self.rpc.update(
                    details=f"Editing {filename}",
                    state="In editor",
                    large_image="m5rcode_logo",   # big icon stays the same
                    large_text="m5rcode Shell",
                    small_image="editing_icon",   # small icon changes for editing
                    small_text="Editing File"
                )
            except Exception:
                self.rpc_active = False

    def _set_running_presence(self, command_name):
        if self.rpc_active and self.rpc:
            try:
                self.rpc.update(
                    details=f"Running {command_name}",
                    state="Executing command",
                    large_image="m5rcode_logo",  # big icon stays the same
                    large_text="m5rcode Shell",
                    small_image="running_icon",  # small icon changes for running
                    small_text="Command Running"
                )
            except Exception:
                self.rpc_active = False

    def _clear_presence(self):
        if self.rpc_active and self.rpc:
            try:
                self.rpc.clear()
            except Exception:
                self.rpc_active = False

    def _close_rpc(self):
        if self.rpc_active and self.rpc:
            try:
                self.rpc.close()
            except Exception:
                pass
            self.rpc_active = False

    # --- Prompt & banners ---
    def update_prompt(self):
        self.prompt = (
            Fore.CYAN
            + "╭─[" + Fore.MAGENTA + "m5rcode" + Fore.CYAN + "] "
            + Fore.YELLOW + self.cwd
            + "\n╰─> "
            + Style.RESET_ALL
        )

    def preloop(self):
        self._print_banner()
        if self.rpc_active:
            self._set_idle_presence()

    def _print_banner(self):
        print(Fore.GREEN + "╔" + "═" * 50 + "╗")
        ascii_art = Figlet(font='slant')
        print(Fore.CYAN + ascii_art.renderText("m5rcode"))
        print(Fore.GREEN + "║ Welcome to m5rcode shell! Type help or ? to list commands.")
        print("╚" + "═" * 50 + "╝" + Style.RESET_ALL)

    def postcmd(self, stop, line):
        if self.rpc_active:
            self._set_idle_presence()
        return stop

    def emptyline(self):
        pass

    def default(self, line):
        print(Fore.RED + Style.BRIGHT + f"Error: Command '{line}' not found." + Style.RESET_ALL)
        print(Fore.YELLOW + "Type 'help' or '?' to see available commands." + Style.RESET_ALL)

    # --- Help styling ---
    def do_help(self, arg):
        if arg:
            super().do_help(arg)
        else:
            print("\n" + Fore.LIGHTCYAN_EX + "─" * 40)
            print(Fore.LIGHTCYAN_EX + " " * 15 + "M5R COMMANDS")
            print(Fore.LIGHTCYAN_EX + "─" * 40 + Style.RESET_ALL)

            print(Fore.YELLOW + "\n── File/Project Commands ──" + Style.RESET_ALL)
            self._print_command_help("new", "Create a new .m5r file")
            self._print_command_help("nano", "Edit a file with your editor")
            self._print_command_help("run", "Run a .m5r script (executes only Python blocks)")

            print(Fore.YELLOW + "\n── Information Commands ──" + Style.RESET_ALL)
            self._print_command_help("fastfetch", "Show language & system info")
            self._print_command_help("credits", "Show project credits")

            print(Fore.YELLOW + "\n── Navigation & Utility ──" + Style.RESET_ALL)
            self._print_command_help("cd", "Change directory within m5rcode/files")
            self._print_command_help("dir", "List files in the current directory")
            self._print_command_help("wdir", "List files hosted at a website directory")
            self._print_command_help("clear", "Clear the shell output")
            self._print_command_help("exit", "Exit the m5rcode shell")
            self._print_command_help("help", "Display this help message")
            self._print_command_help("?", "Alias for 'help'")

            print("\n" + Fore.LIGHTCYAN_EX + "─" * 40 + Style.RESET_ALL)
            print(Fore.LIGHTBLACK_EX + "For detailed help on a command, type: " + Fore.CYAN + "help <command>" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "─" * 40 + Style.RESET_ALL + "\n")

    def _print_command_help(self, command, description):
        print(f"  {Fore.GREEN}{command:<12}{Style.RESET_ALL} {Fore.WHITE}→ {description}{Style.RESET_ALL}")

    # --- Commands ---
    def do_clear(self, arg):
        os.system('cls' if os.name == 'nt' else 'clear')
        self._print_banner()
        self.update_prompt()

    def do_new(self, arg):
        if self.rpc_active:
            self._set_running_presence("new file")
        NewCommand(self.cwd, arg.strip()).run()

    def do_nano(self, arg):
        filename = arg.strip()
        if self.rpc_active:
            self._set_editing_presence(filename)
        NanoCommand(self.cwd, filename).run()

    def do_run(self, arg):
        if self.rpc_active:
            self._set_running_presence(f"script {arg.strip()}")
        RunCommand(self.cwd, arg.strip()).run()

    def do_fastfetch(self, arg):
        if self.rpc_active:
            self._set_running_presence("fastfetch")
        FastfetchCommand().run()

    def do_credits(self, arg):
        if self.rpc_active:
            self._set_running_presence("credits")
        CreditsCommand().run()

    def do_cd(self, arg):
        if self.rpc_active:
            self._set_running_presence(f"changing directory to {arg.strip()}")
        CdCommand(self.base_dir, [self], arg).run()
        os.chdir(self.cwd)
        self.update_prompt()

    def do_dir(self, arg):
        if self.rpc_active:
            self._set_running_presence("dir")
        try:
            files = os.listdir(self.cwd)
            if not files:
                print(Fore.YELLOW + "Directory is empty." + Style.RESET_ALL)
                return
            print(Fore.GREEN + "\nFiles in directory:" + Style.RESET_ALL)
            for f in files:
                path = os.path.join(self.cwd, f)
                if os.path.isdir(path):
                    print(f"  {Fore.CYAN}{f}/ {Style.RESET_ALL}")
                else:
                    print(f"  {Fore.WHITE}{f}{Style.RESET_ALL}")
        except Exception as e:
            print(Fore.RED + f"[ERR] {e}" + Style.RESET_ALL)

    def do_wdir(self, arg):
        if self.rpc_active:
            self._set_running_presence("wdir")
        WdirCommand(arg).run()

    def do_exit(self, arg):
        self._clear_presence()
        self._close_rpc()
        return ExitCommand().run()

if __name__ == "__main__":
    M5RShell().cmdloop()
