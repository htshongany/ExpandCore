import os
import sys
import sqlite3
from datetime import datetime
from rich.console import Console
from rich.table import Table
from config import DATABASE
from modules.url_todo_list.utils import (
    is_valid_url, export_to_csv, export_to_json, export_to_xml
)

console = Console()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_for_error():
    console.print("[bold blue]Press any key to continue...[/bold blue]")
    input()

def get_database_path(db_name=None):
    """Get the path to the database file. If not defined, use 'todos.db'."""
    if db_name != None:
        return db_name
    else:
        return os.path.join(os.path.dirname(__file__), 'todos.db')


def create_connection(db_file):
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        console.print(f"[bold red]Failed to create connection to database {db_file}: {e}[/bold red]")
        return conn

def initialize_database(conn):
    """Initialize the database with the required table if it doesn't exist"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        description TEXT,
        category TEXT,
        status BOOLEAN NOT NULL CHECK (status IN (0, 1))
    );
    """
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
        conn.commit()
    except sqlite3.Error as e:
        console.print(f"[bold red]Failed to initialize database: {e}[/bold red]")

def fetch_all_urls(conn):
    """Fetch all URLs from the table"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM urls")
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as e:
        console.print(f"[bold red]Failed to fetch all URLs: {e}[/bold red]")
        return []

def fetch_urls_by_status(conn, status):
    """Fetch URLs by status"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM urls WHERE status=?", (status,))
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as e:
        console.print(f"[bold red]Failed to fetch URLs by status: {e}[/bold red]")
        return []

def fetch_urls_by_category(conn, category):
    """Fetch URLs by category"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM urls WHERE category=?", (category,))
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as e:
        console.print(f"[bold red]Failed to fetch URLs by category: {e}[/bold red]")
        return []

def add_url(conn):
    """Add a new URL to the table"""
    clear_console()
    url = console.input("\n[bold yellow]Enter the URL:[/bold yellow] ")
    description = console.input("\n[bold yellow]Enter the description:[/bold yellow] ")
    category = console.input("\n[bold yellow]Enter the category:[/bold yellow] ")

    if not is_valid_url(url):
        console.print("[bold red]Invalid URL format.[/bold red]")
        pause_for_error()
        return

    sql = ''' INSERT INTO urls(url, description, category, status)
              VALUES(?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (url, description, category, False))
        conn.commit()
        console.print(f"[bold green]URL '{url}' added successfully![/bold green]")
    except sqlite3.Error as e:
        console.print(f"[bold red]Failed to add URL: {e}[/bold red]")
    finally:
        pause_for_error()

def delete_url(conn):
    """Delete a URL from the table by its ID"""
    clear_console()
    console.print("\n[bold cyan]Existing URLs:[/bold cyan]")
    urls = fetch_all_urls(conn)
    if urls:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=6)
        table.add_column("URL", justify="left")
        table.add_column("Description", justify="left")
        table.add_column("Category", justify="left")
        table.add_column("Status", justify="left")
        for row in urls:
            table.add_row(str(row[0]), row[1], row[2], row[3], str(row[4]))
        console.print(table)
    else:
        console.print("[bold red]No URLs found.[/bold red]")
        pause_for_error()
        return

    url_id = console.input("\n[bold yellow]Enter the ID of the URL to delete:[/bold yellow] ")
    sql = ''' DELETE FROM urls WHERE id=? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (url_id,))
        conn.commit()
        console.print(f"[bold green]URL with ID {url_id} deleted successfully![bold green]")
    except sqlite3.Error as e:
        console.print(f"[bold red]Failed to delete URL: {e}[/bold red]")
    finally:
        pause_for_error()

def update_url(conn):
    """Update the description and/or status of a URL"""
    clear_console()
    console.print("\n[bold cyan]Existing URLs:[/bold cyan]")
    urls = fetch_all_urls(conn)
    if urls:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=6)
        table.add_column("URL", justify="left")
        table.add_column("Description", justify="left")
        table.add_column("Category", justify="left")
        table.add_column("Status", justify="left")
        for row in urls:
            table.add_row(str(row[0]), row[1], row[2], row[3], str(row[4]))
        console.print(table)
    else:
        console.print("[bold red]No URLs found.[/bold red]")
        pause_for_error()
        return

    url_id = console.input("\n[bold yellow]Enter the ID of the URL to update:[/bold yellow] ")
    description = console.input("\n[bold yellow]Enter new description (leave blank to keep the same):[/bold yellow] ")
    status_input = console.input("\n[bold yellow]Enter new status (True/False) (leave blank to keep the same):[/bold yellow] ")

    # Prepare the SQL update
    sql = "UPDATE urls SET "
    params = []

    if description:
        sql += "description = ?, "
        params.append(description)

    if status_input:
        sql += "status = ?, "
        params.append(status_input.lower() == 'true')

    sql = sql.rstrip(', ')  # Remove the trailing comma
    sql += " WHERE id = ?"
    params.append(url_id)

    try:
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        conn.commit()
        console.print(f"[bold green]URL with ID {url_id} updated successfully![bold green]")
    except sqlite3.Error as e:
        console.print(f"[bold red]Failed to update URL: {e}[/bold red]")
    finally:
        pause_for_error()

def view_urls(conn):
    """View URLs with different filters"""
    clear_console()
    console.print("\n[bold cyan]View Options:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option", style="dim", width=12)
    table.add_column("View Type", justify="left")

    view_options = {
        "1": "All URLs",
        "2": "Read URLs",
        "3": "Unread URLs",
        "4": "By Category"
    }

    for key, option in view_options.items():
        table.add_row(key, option)

    console.print(table)

    choice = console.input("\n[bold yellow]Select a view option:[/bold yellow] ")

    if choice == "1":
        urls = fetch_all_urls(conn)
    elif choice == "2":
        urls = fetch_urls_by_status(conn, True)
    elif choice == "3":
        urls = fetch_urls_by_status(conn, False)
    elif choice == "4":
        category = console.input("\n[bold yellow]Enter the category:[/bold yellow] ")
        urls = fetch_urls_by_category(conn, category)
    else:
        console.print("[bold red]Invalid selection.[/bold red]")
        pause_for_error()
        return

    if urls:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=6)
        table.add_column("URL", justify="left")
        table.add_column("Description", justify="left")
        table.add_column("Category", justify="left")
        table.add_column("Status", justify="left")

        for row in urls:
            table.add_row(str(row[0]), row[1], row[2], row[3], str(row[4]))

        console.print(table)
    else:
        console.print("[bold red]No URLs found.[/bold red]")
        # pause_for_error(False)
    pause_for_error()

def export_urls(conn):
    """Export URLs to a file"""
    clear_console()
    console.print("\n[bold cyan]Export Options:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option", style="dim", width=12)
    table.add_column("Format", justify="left")

    export_options = {
        "1": "CSV",
        "2": "JSON",
        "3": "XML"
    }

    for key, option in export_options.items():
        table.add_row(key, option)

    console.print(table)

    choice = console.input("\n[bold yellow]Select an export format:[/bold yellow] ")
    filename = console.input("\n[bold yellow]Enter the filename:[/bold yellow] ")

    urls = fetch_all_urls(conn)
    if choice == "1":
        export_to_csv(urls, filename)
    elif choice == "2":
        export_to_json(urls, filename)
    elif choice == "3":
        export_to_xml(urls, filename)
    else:
        console.print("[bold red]Invalid export format.[/bold red]")
        pause_for_error()
        return

    console.print(f"[bold green]URLs exported successfully to {filename}.[/bold green]")
    pause_for_error()

def run():
    # Get the database path
    db_path = get_database_path(DATABASE)
    conn = create_connection(db_path)
    if not conn:
        return

    # Initialize the database
    initialize_database(conn)

    while True:
        # Interactive Console Menu
        clear_console()
        console.print("\n[bold cyan]Main Menu:[/bold cyan]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="dim", width=12)
        table.add_column("Action", justify="left")

        main_options = {
            "1": "Add URL",
            "2": "Delete URL",
            "3": "View URLs",
            "4": "Update URL",
            "5": "Export URLs",
            "6": "Exit"
        }

        for key, option in main_options.items():
            table.add_row(key, option)

        console.print(table)

        choice = console.input("\n[bold yellow]Select an option:[/bold yellow] ")

        if choice == "1":
            add_url(conn)
        elif choice == "2":
            delete_url(conn)
        elif choice == "3":
            view_urls(conn)
        elif choice == "4":
            update_url(conn)
        elif choice == "5":
            export_urls(conn)
        elif choice == "6":
            console.print("[bold cyan]Exiting...[/bold cyan]")
            break
        else:
            console.print("[bold red]Invalid selection.[/bold red]")
            pause_for_error()

if __name__ == "__main__":
    run()