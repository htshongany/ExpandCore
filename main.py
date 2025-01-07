import os
import sys
from core.manager import ModuleManager
from config import MODULES, MAX_ATTEMPTS, START_INDEX
from rich.console import Console
from rich.table import Table

console = Console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_for_error():
    console.print("[bold blue]Press any key to continue...[/bold blue]")
    input()

def main():
    manager = ModuleManager()
    for module in MODULES.values():
        manager.load_module(module)

    if len(MODULES) == 1:
        module_name = list(MODULES.values())[0]
        if module_name in manager.modules:
            manager.modules[module_name].main()
    else:
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            clear_console()
            console.print("\n[bold cyan]Available Modules:[/bold cyan]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Option", style="dim", width=12)
            table.add_column("Module", justify="left")

            for key, module in MODULES.items():
                table.add_row(key, module)
            
            console.print(table)

            choice = console.input(f"\n[bold yellow]Select a module to run (between {START_INDEX} and {START_INDEX + len(MODULES) - 1}):[/bold yellow] ")
            try:
                if choice in MODULES:
                    module_name = MODULES[choice]
                    if module_name in manager.modules:
                        manager.modules[module_name].main()
                        return
                    else:
                        console.print("[bold red]The module is not loaded properly.[/bold red]")
                        pause_for_error()
                else:
                    raise ValueError
            except ValueError:
                console.print(f"[bold red]Invalid selection. Please enter a number between {START_INDEX} and {START_INDEX + len(MODULES) - 1}.[/bold red]")
                attempts += 1
                pause_for_error()

        console.print("[bold yellow]Maximum attempts reached. Exiting.[/bold yellow]")
        sys.exit(1)

if __name__ == '__main__':
    main()
