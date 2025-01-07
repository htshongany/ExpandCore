import sqlite3
import csv
import json
import re
import xml.etree.ElementTree as ET

def is_valid_url(url):
    """Check if a string is a valid URL"""
    regex = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'([a-zA-Z0-9-]{1,63}\.)+'  # domain...
        r'[a-zA-Z]{2,6}'  # top-level domain
        r'(:\d+)?'  # optional port
        r'(/.*)?$', re.IGNORECASE)  # optional path
    return re.match(regex, url) is not None

def export_to_csv(data, filename):
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "URL", "Description", "Category", "Status", "Timestamp"])
            writer.writerows(data)
        print(f"Data exported to {filename} successfully!")
    except Exception as e:
        print(f"Failed to export data to {filename}: {e}")

def export_to_json(data, filename):
    try:
        with open(filename, 'w') as file:
            json_data = [
                {"ID": row[0], "URL": row[1], "Description": row[2], "Category": row[3], "Status": row[4], "Timestamp": row[5]}
                for row in data
            ]
            json.dump(json_data, file, indent=4)
        print(f"Data exported to {filename} successfully!")
    except Exception as e:
        print(f"Failed to export data to {filename}: {e}")

def export_to_xml(data, filename):
    try:
        root = ET.Element("urls")
        for row in data:
            url_elem = ET.SubElement(root, "url")
            ET.SubElement(url_elem, "ID").text = str(row[0])
            ET.SubElement(url_elem, "URL").text = row[1]
            ET.SubElement(url_elem, "Description").text = row[2]
            ET.SubElement(url_elem, "Category").text = row[3]
            ET.SubElement(url_elem, "Status").text = str(row[4])
            ET.SubElement(url_elem, "Timestamp").text = row[5]
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f"Data exported to {filename} successfully!")
    except Exception as e:
        print(f"Failed to export data to {filename}: {e}")

def push_to_database(conn, data, format):
    """Push data to database based on format"""
    try:
        if format == 'csv':
            with open(data, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    add_url(conn, row[1], row[2], row[3])
        elif format == 'json':
            with open(data, 'r') as file:
                json_data = json.load(file)
                for entry in json_data:
                    add_url(conn, entry['URL'], entry['Description'], entry['Category'])
        elif format == 'xml':
            tree = ET.parse(data)
            root = tree.getroot()
            for url_elem in root.findall('url'):
                url = url_elem.find('URL').text
                description = url_elem.find('Description').text
                category = url_elem.find('Category').text
                add_url(conn, url, description, category)
        print("Data pushed to the database successfully!")
    except Exception as e:
        print(f"Failed to push data to the database: {e}")

def add_url(conn, url, description, category):
    """Add a new URL to the table"""
    if url_exists(conn, url):
        print(f"Warning: URL '{url}' already exists.")
        return None
    sql = ''' INSERT INTO urls(url, description, category, status)
              VALUES(?,?,?,?) '''
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
    sql = ''' SELECT 1 FROM urls WHERE url=? '''
    cur = conn.cursor()
    cur.execute(sql, (url,))
    return cur.fetchone() is not None
