from colorama import Fore

class ExitCommand:
    def run(self):
        print(Fore.YELLOW + "Bye!")
        return True  # Signals to shell to exit
