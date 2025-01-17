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

def export_to_csv(urls, filename):
    """Export URLs to a CSV file"""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "URL", "Description", "Category", "Status"])
        for url in urls:
            writer.writerow(url)

def export_to_json(urls, filename):
    """Export URLs to a JSON file"""
    with open(filename, 'w') as file:
        json.dump([{
            "ID": url[0],
            "URL": url[1],
            "Description": url[2],
            "Category": url[3],
            "Status": url[4]
        } for url in urls], file, indent=4)

def export_to_xml(urls, filename):
    """Export URLs to an XML file"""
    root = ET.Element("urls")
    for url in urls:
        url_element = ET.SubElement(root, "url")
        ET.SubElement(url_element, "ID").text = str(url[0])
        ET.SubElement(url_element, "URL").text = url[1]
        ET.SubElement(url_element, "Description").text = url[2]
        ET.SubElement(url_element, "Category").text = url[3]
        ET.SubElement(url_element, "Status").text = str(url[4])

    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

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
