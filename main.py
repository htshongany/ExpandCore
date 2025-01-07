import os
import sys
from core.manager import ModuleManager
from config import MODULES, MAX_ATTEMPTS, START_INDEX
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_for_error():
    console.print("[bold blue]Press any key to continue...[/bold blue]")
    input()

def display_modules_table(modules):
    """Display a table of available modules."""
    if not modules:
        console.print(Panel("[bold red]No modules available![/bold red]", title="[bold yellow]Module Manager[/bold yellow]"))
        return False

    console.print("\n[bold cyan]Available Modules:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option", style="dim", width=12)
    table.add_column("Module", justify="left")

    index_offset = START_INDEX
    for i, (key, module) in enumerate(modules.items(), start=index_offset):
        table.add_row(str(i), module)
    table.add_row(str(index_offset + len(modules)), "[bold red]Exit[/bold red]")

    console.print(table)
    return True

def main():
    # Initialize the ModuleManager and load modules
    manager = ModuleManager()
    for module in MODULES.values():
        manager.load_module(module)

    if not MODULES:
        console.print(Panel("[bold red]No modules have been configured in MODULES![/bold red]", title="[bold yellow]Error[/bold yellow]"))
        sys.exit(1)

    attempts = 0  # Track invalid attempts

    # Main menu loop
    while attempts < MAX_ATTEMPTS:
        clear_console()
        if not display_modules_table(MODULES):
            sys.exit(1)

        choice = console.input(f"\n[bold yellow]Select a module to run or {START_INDEX + len(MODULES)} to exit:[/bold yellow] ")
        try:
            if choice.isdigit():
                choice = int(choice)
                if START_INDEX <= choice < START_INDEX + len(MODULES):
                    module_name = list(MODULES.values())[choice - START_INDEX]
                    if module_name in manager.modules:
                        # Run the module's main function
                        console.print(f"[bold cyan]Launching module: {module_name}[/bold cyan]")
                        manager.modules[module_name].main()
                        attempts = 0  # Reset attempts after a successful execution
                    else:
                        console.print("[bold red]The module is not loaded properly.[/bold red]")
                        pause_for_error()
                elif choice == START_INDEX + len(MODULES):
                    console.print("[bold yellow]Exiting the menu. Goodbye![/bold yellow]")
                    sys.exit(0)
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            attempts += 1
            console.print(f"[bold red]Invalid selection. Please enter a valid option ({MAX_ATTEMPTS - attempts} attempts remaining).[/bold red]")
            pause_for_error()

    console.print("[bold yellow]Maximum attempts reached. Exiting the program.[/bold yellow]")
    sys.exit(1)

if __name__ == '__main__':
    main()
