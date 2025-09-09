import os
from colorama import Fore

class DirCommand:
    def __init__(self, cwd, target):
        self.cwd = cwd
        self.target = target if target else cwd

    def run(self):
        path = os.path.abspath(os.path.join(self.cwd, self.target))

        if not os.path.exists(path):
            print(Fore.RED + f"No such file or directory: {self.target}")
            return

        if os.path.isfile(path):
            print(Fore.GREEN + f"{self.target} (file)")
            return

        print(Fore.CYAN + f"Directory listing for {path}:\n")
        try:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    print(Fore.BLUE + f"[DIR]  {item}")
                else:
                    print(Fore.GREEN + f"[FILE] {item}")
        except PermissionError:
            print(Fore.RED + "Access denied.")
