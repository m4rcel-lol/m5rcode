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

# Initialize colorama for colored terminal output
init(autoreset=True)

# --- Discord RPC Configuration ---
CLIENT_ID = '1414669512158220409' # Your Discord Application ID

class M5RShell(cmd.Cmd):
    """
    An interactive shell for m5rcode projects with Discord Rich Presence integration.
    """
    def __init__(self):
        super().__init__()
        self.base_dir = os.path.join(os.path.expanduser("~"), "m5rcode", "files")
        os.makedirs(self.base_dir, exist_ok=True)

        self.cwd = self.base_dir
        os.chdir(self.cwd)

        self.update_prompt()

        # --- Discord RPC Initialization ---
        self.rpc_active = False
        self.rpc = None
        self._connect_rpc()

        if self.rpc_active:
            self._set_idle_presence()

    def _connect_rpc(self):
        """Attempts to connect to Discord RPC."""
        try:
            self.rpc = Presence(CLIENT_ID)
            self.rpc.connect()
            self.rpc_active = True
        except exceptions.DiscordNotFound:
            print(Fore.YELLOW + "[RPC] Discord client not found. Rich Presence will not be active." + Style.RESET_ALL)
            self.rpc_active = False
            self.rpc = None
        except Exception as e:
            print(Fore.RED + f"[RPC Error] Could not connect to Discord RPC: {e}" + Style.RESET_ALL)
            self.rpc_active = False
            self.rpc = None

    def _set_idle_presence(self):
        """Sets the RPC status to 'Using the shell'."""
        if self.rpc_active and self.rpc:
            try:
                self.rpc.update(
                    details="Using the shell",
                    state="Waiting for commands...",
                    small_image="shell",
                    small_text="Shell (Idle)"
                )
            except Exception as e:
                print(Fore.RED + f"[RPC Error] Could not update idle presence: {e}" + Style.RESET_ALL)
                self.rpc_active = False
                self.rpc = None

    def _set_editing_presence(self, filename):
        """Sets the RPC status to 'Editing [filename]'."""
        if self.rpc_active and self.rpc:
            try:
                self.rpc.update(
                    details=f"Editing {filename}",
                    state="In editor",
                    small_image="shell_editing",
                    small_text="Editing File"
                )
            except Exception as e:
                print(Fore.RED + f"[RPC Error] Could not update editing presence: {e}" + Style.RESET_ALL)
                self.rpc_active = False
                self.rpc = None

    def _set_running_presence(self, command_name):
        """Sets the RPC status to 'Running [command_name]'."""
        if self.rpc_active and self.rpc:
            try:
                self.rpc.update(
                    details=f"Running {command_name}",
                    state="Executing command",
                    small_image="shell_running",
                    small_text="Command Running"
                )
            except Exception as e:
                print(Fore.RED + f"[RPC Error] Could not update running presence: {e}" + Style.RESET_ALL)
                self.rpc_active = False
                self.rpc = None

    def _clear_presence(self):
        """Clears the current RPC status."""
        if self.rpc_active and self.rpc:
            try:
                self.rpc.clear()
            except Exception as e:
                print(Fore.RED + f"[RPC Error] Could not clear presence: {e}" + Style.RESET_ALL)
                self.rpc_active = False
                self.rpc = None

    def _close_rpc(self):
        """Closes the Discord RPC connection."""
        if self.rpc_active and self.rpc:
            try:
                self.rpc.close()
            except Exception as e:
                print(Fore.RED + f"[RPC Error] Could not close RPC: {e}" + Style.RESET_ALL)
            finally:
                self.rpc_active = False
                self.rpc = None

    def update_prompt(self):
        """Refresh the prompt to reflect the current working directory."""
        self.prompt = (
            Fore.CYAN
            + "╭─[" + Fore.MAGENTA + "m5rcode" + Fore.CYAN + "] "
            + Fore.YELLOW + self.cwd
            + "\n╰─> "
            + Style.RESET_ALL
        )

    def preloop(self):
        """Called once before the command loop starts."""
        self._print_banner()
        if self.rpc_active:
            self._set_idle_presence()

    def _print_banner(self):
        """Prints the initial shell banner."""
        print(Fore.GREEN + "╔" + "═" * 50 + "╗")
        ascii_art = Figlet(font='slant')
        print(Fore.CYAN + ascii_art.renderText("m5rcode"))
        print(Fore.GREEN + "║ Welcome to m5rcode shell! Type help or ? to list commands.")
        print("╚" + "═" * 50 + "╝" + Style.RESET_ALL) # Added Style.RESET_ALL here

    def postcmd(self, stop, line):
        """
        Called after a command has been executed.
        Resets RPC to idle state after any command completes.
        """
        if self.rpc_active:
            self._set_idle_presence()
        return stop

    # --- Error Handling Styling ---
    def emptyline(self):
        """Do nothing on empty input line."""
        pass # Simply do nothing instead of repeating the last command

    def default(self, line):
        """
        Called when the command is not recognized.
        Prints a styled error message.
        """
        print(Fore.RED + Style.BRIGHT + f"Error: Command '{line}' not found." + Style.RESET_ALL)
        print(Fore.YELLOW + "Type 'help' or '?' to see available commands." + Style.RESET_ALL)

    # --- Help Command Styling ---
    def do_help(self, arg):
        """
        Displays help information for commands.
        Type 'help' or '?' for a list of commands.
        Type 'help <command>' for detailed help on a specific command.
        """
        if arg:
            # If an argument is provided, call the default help behavior for that command
            super().do_help(arg)
        else:
            # Custom help output for all commands
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

            print(Fore.YELLOW + "\n── Navigation & Utility ──" + Style.RESET_ALL) # Renamed category
            self._print_command_help("cd", "Change directory within m5rcode/files")
            self._print_command_help("clear", "Clear the shell output") # Added clear to help
            self._print_command_help("exit", "Exit the m5rcode shell")
            self._print_command_help("help", "Display this help message")
            self._print_command_help("?", "Alias for 'help'")

            print("\n" + Fore.LIGHTCYAN_EX + "─" * 40 + Style.RESET_ALL)
            print(Fore.LIGHTBLACK_EX + "For detailed help on a command, type: " + Fore.CYAN + "help <command>" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "─" * 40 + Style.RESET_ALL + "\n")

    def _print_command_help(self, command, description):
        """Helper to print a single command's help in a formatted way."""
        print(f"  {Fore.GREEN}{command:<12}{Style.RESET_ALL} {Fore.WHITE}→ {description}{Style.RESET_ALL}")

    # --- New Clear Command ---
    def do_clear(self, arg):
        """clear   → Clear the shell output"""
        os.system('cls' if os.name == 'nt' else 'clear')
        self._print_banner() # Re-print the banner after clearing
        self.update_prompt() # Ensure prompt is updated and displayed

    # ── File/project commands ─────────────────────────────────────────────────

    def do_new(self, arg):
        """new <filename>   → create a new .m5r file"""
        if self.rpc_active:
            self._set_running_presence("new file")
        NewCommand(self.cwd, arg.strip()).run()

    def do_nano(self, arg):
        """nano <filename>   → edit a file with your editor"""
        filename = arg.strip()
        if self.rpc_active:
            self._set_editing_presence(filename)
        NanoCommand(self.cwd, filename).run()

    def do_run(self, arg):
        """run <filename>   → run a .m5r script (executes only Python blocks)"""
        if self.rpc_active:
            self._set_running_presence(f"script {arg.strip()}")
        RunCommand(self.cwd, arg.strip()).run()

    def do_fastfetch(self, arg):
        """fastfetch   → show language & system info"""
        if self.rpc_active:
            self._set_running_presence("fastfetch")
        FastfetchCommand().run()

    def do_credits(self, arg):
        """credits   → show project credits"""
        if self.rpc_active:
            self._set_running_presence("credits")
        CreditsCommand().run()

    # ── Navigation & exit ────────────────────────────────────────────────────

    def do_cd(self, arg):
        """cd <directory>   → change directory within m5rcode/files"""
        if self.rpc_active:
            self._set_running_presence(f"changing directory to {arg.strip()}")
        CdCommand(self.base_dir, [self], arg).run()
        os.chdir(self.cwd)
        self.update_prompt()

    def do_exit(self, arg):
        """exit   → exit the m5rcode shell"""
        self._clear_presence()
        self._close_rpc()
        return ExitCommand().run()

if __name__ == "__main__":
    M5RShell().cmdloop()
