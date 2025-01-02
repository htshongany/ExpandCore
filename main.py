# main.py

from core.manager import ModuleManager
from config import MODULES
from rich.console import Console
from rich.table import Table

console = Console()

def main():
    manager = ModuleManager()
    for module in MODULES.values():
        manager.load_module(module)

    if len(MODULES) == 1:
        module_name = list(MODULES.values())[0]
        if module_name in manager.modules:
            manager.modules[module_name].main()
    else:
        console.print("\n[bold cyan]Available Modules:[/bold cyan]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="dim", width=12)
        table.add_column("Module", justify="left")

        for key, module in MODULES.items():
            table.add_row(key, module)
        
        console.print(table)

        choice = console.input("\n[bold yellow]Select a module to run (by number):[/bold yellow] ")

        if choice in MODULES:
            module_name = MODULES[choice]
            if module_name in manager.modules:
                manager.modules[module_name].main()
        else:
            console.print("[bold red]Invalid module selection.[/bold red]")

if __name__ == '__main__':
    main()
