import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Failed to create connection to database {db_file}: {e}")
    return conn

def create_table(conn):
    """Create a table for URLs"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL UNIQUE,
        description TEXT,
        status BOOLEAN DEFAULT 0,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(f"Failed to create table: {e}")

def add_url(conn, url, description):
    """Add a new URL to the table"""
    if url_exists(conn, url):
        print(f"Warning: URL '{url}' already exists.")
        return None
    sql = ''' INSERT INTO urls(url, description, status)
              VALUES(?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (url, description, False))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Failed to add URL: {e}")
        return None

def url_exists(conn, url):
    """Check if a URL already exists in the table"""
    sql = ''' SELECT 1 FROM urls WHERE url=? '''
    cur = conn.cursor()
    cur.execute(sql, (url,))
    return cur.fetchone() is not None

def update_url_status(conn, url_id, status):
    """Update the status of a URL"""
    sql = ''' UPDATE urls
              SET status = ?
              WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (status, url_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Failed to update URL status: {e}")

def fetch_all_urls(conn):
    """Fetch all URLs from the table"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM urls")
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Failed to fetch all URLs: {e}")
        return []

def fetch_urls_by_status(conn, status):
    """Fetch URLs by status"""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM urls WHERE status=?", (status,))
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Failed to fetch URLs by status: {e}")
        return []

def delete_url(conn, url_id):
    """Delete a URL from the table by its ID"""
    sql = ''' DELETE FROM urls WHERE id=? '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (url_id,))
        conn.commit()
        print(f"URL with ID {url_id} deleted successfully!")
    except sqlite3.Error as e:
        print(f"Failed to delete URL: {e}")
