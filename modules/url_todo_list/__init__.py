from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from core.notifications import send_notification
from .database import create_connection, create_table, add_url, update_url_status, fetch_all_urls, fetch_urls_by_status, delete_url
from .utils import export_to_csv, is_valid_url
from config import DATABASE

name = "Test Module"
version = "1.0.0"

console = Console()

def main():
    db_file = DATABASE # Nom du fichier de la base de données
    try:
        conn = create_connection(db_file)
        create_table(conn)

        while True:
            show_menu()

            choice = Prompt.ask("[bold yellow]Choose an option[/bold yellow]")

            if choice == "1":
                add_url_console(conn)
            elif choice == "2":
                display_all_urls(conn)
            elif choice == "3":
                mark_url_as_read(conn)
            elif choice == "4":
                mark_url_as_unread(conn)
            elif choice == "5":
                display_urls_by_status(conn, True)
            elif choice == "6":
                display_urls_by_status(conn, False)
            elif choice == "7":
                send_notification_for_url(conn)
            elif choice == "8":
                export_urls_to_csv_console(conn)
            elif choice == "9":
                delete_url_console(conn)
            elif choice == "10":
                break
            else:
                console.print("[bold red]Invalid option. Please choose a valid option.[/bold red]")
            
            if choice != "10":
                console.input("Press Enter to continue...")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

def show_menu():
    console.clear()
    table = Table(title="[bold cyan]URL TODO LIST[/bold cyan]", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="dim", width=7)
    table.add_column("Description", justify="left")

    table.add_row("1", "Add URL")
    table.add_row("2", "View All URLs")
    table.add_row("3", "Mark URL as Read")
    table.add_row("4", "Mark URL as Unread")
    table.add_row("5", "View Read URLs")
    table.add_row("6", "View Unread URLs")
    table.add_row("7", "Send Notification for URL")
    table.add_row("8", "Export URLs to CSV")
    table.add_row("9", "Delete URL")
    table.add_row("10", "Exit")

    console.print(table)

def add_url_console(conn):
    try:
        url = Prompt.ask("Enter the URL")
        if not is_valid_url(url):
            console.print(f"[bold yellow]Warning: '{url}' is not a valid URL.[/bold yellow]")
            return
        description = Prompt.ask("Enter a description")
        if add_url(conn, url, description) is None:
            console.print(f"[bold yellow]Warning: URL '{url}' already exists.[/bold yellow]")
            return
        console.print("[bold green]URL added successfully![bold green]")
        display_all_urls(conn)
    except Exception as e:
        console.print(f"[bold red]Failed to add URL: {e}[/bold red]")

def display_all_urls(conn):
    try:
        console.clear()
        rows = fetch_all_urls(conn)
        table = Table(title="All URLs")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("URL", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Status", style="blue")
        table.add_column("Timestamp", style="yellow")

        for row in rows:
            status = "Read" if row[3] else "Unread"
            table.add_row(str(row[0]), row[1], row[2], status, row[4])

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Failed to display URLs: {e}[/bold red]")

def mark_url_as_read(conn):
    try:
        url_id = int(Prompt.ask("Enter the ID of the URL to mark as read"))
        update_url_status(conn, url_id, True)
        console.print("[bold green]URL marked as read![bold green]")
        display_all_urls(conn)
    except Exception as e:
        console.print(f"[bold red]Failed to mark URL as read: {e}[/bold red]")

def mark_url_as_unread(conn):
    try:
        url_id = int(Prompt.ask("Enter the ID of the URL to mark as unread"))
        update_url_status(conn, url_id, False)
        console.print("[bold green]URL marked as unread![bold green]")
        display_all_urls(conn)
    except Exception as e:
        console.print(f"[bold red]Failed to mark URL as unread: {e}[/bold red]")

def display_urls_by_status(conn, status):
    try:
        console.clear()
        rows = fetch_urls_by_status(conn, status)
        table = Table(title="Read URLs" if status else "Unread URLs")
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("URL", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Timestamp", style="yellow")

        for row in rows:
            table.add_row(str(row[0]), row[1], row[2], row[4])

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Failed to display URLs by status: {e}[/bold red]")

def send_notification_for_url(conn):
    try:
        url_id = int(Prompt.ask("Enter the ID of the URL for sending notification"))
        url = fetch_all_urls(conn)[url_id - 1]
        send_notification("Reading Reminder", f"Read URL: {url[1]}")
        console.print("[bold green]Notification sent![bold green]")
    except Exception as e:
        console.print(f"[bold red]Failed to send notification: {e}[/bold red]")

def export_urls_to_csv_console(conn):
    try:
        rows = fetch_all_urls(conn)
        filename = Prompt.ask("Enter the filename (with .csv extension)")
        export_to_csv(rows, filename)
        console.print(f"[bold green]Data exported to {filename}![bold green]")
    except Exception as e:
        console.print(f"[bold red]Failed to export data to {filename}: {e}[/bold red]")

def delete_url_console(conn):
    try:
        url_id = int(Prompt.ask("Enter the ID of the URL to delete"))
        delete_url(conn, url_id)
        display_all_urls(conn)
    except Exception as e:
        console.print(f"[bold red]Failed to delete URL: {e}[/bold red]")

if __name__ == '__main__':
    main()
