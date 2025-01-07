import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database"""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Failed to create connection to database {db_file}: {e}")
        return None

def create_table(conn):
    """Create a table for URLs"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL UNIQUE,
        description TEXT,
        category TEXT,
        status BOOLEAN DEFAULT 0,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Failed to create table: {e}")

def add_url(conn, url, description, category):
    """Add a new URL to the table"""
    if url_exists(conn, url):
        print(f"Warning: URL '{url}' already exists.")
        return None
    sql = '''INSERT INTO urls(url, description, category, status) VALUES (?, ?, ?, ?)'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (url, description, category, False))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Failed to add URL: {e}")
        return None

def url_exists(conn, url):
    """Check if a URL already exists in the table"""
    sql = '''SELECT 1 FROM urls WHERE url=?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (url,))
        return cur.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Failed to check URL existence: {e}")
        return False

def update_url_status(conn, url_id, status):
    """Update the status of a URL"""
    sql = '''UPDATE urls SET status = ? WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (status, url_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Failed to update URL status: {e}")

def update_url_description(conn, url_id, description):
    """Update the description of a URL"""
    sql = '''UPDATE urls SET description = ? WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (description, url_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Failed to update URL description: {e}")

def fetch_all_urls(conn):
    """Fetch all URLs from the table"""
    sql = '''SELECT * FROM urls'''
    try:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Failed to fetch all URLs: {e}")
        return []

def fetch_urls_by_status(conn, status):
    """Fetch URLs by status"""
    sql = '''SELECT * FROM urls WHERE status = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (status,))
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Failed to fetch URLs by status: {e}")
        return []

def fetch_urls_by_category(conn, category):
    """Fetch URLs by category"""
    sql = '''SELECT * FROM urls WHERE category = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (category,))
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Failed to fetch URLs by category: {e}")
        return []

def delete_url(conn, url_id):
    """Delete a URL from the table by its ID"""
    sql = '''DELETE FROM urls WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (url_id,))
        conn.commit()
        print(f"URL with ID {url_id} deleted successfully!")
    except sqlite3.Error as e:
        print(f"Failed to delete URL: {e}")

def fetch_urls_by_time(conn, start_time, end_time):
    """Fetch URLs by timestamp range"""
    sql = '''SELECT * FROM urls WHERE timestamp BETWEEN ? AND ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (start_time, end_time))
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Failed to fetch URLs by time range: {e}")
        return []
