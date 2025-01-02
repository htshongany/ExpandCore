import unittest
from modules.url_todo_list.database import create_connection, create_table, add_url, fetch_all_urls, update_url_status, fetch_urls_by_status, delete_url
from modules.url_todo_list.utils import is_valid_url

class TestURLManager(unittest.TestCase):

    def setUp(self):
        self.conn = create_connection(":memory:")
        create_table(self.conn)

    def test_add_url(self):
        url_id = add_url(self.conn, "http://example.com", "Example description")
        self.assertIsNotNone(url_id)

    def test_add_duplicate_url(self):
        add_url(self.conn, "http://example.com", "Example description")
        url_id = add_url(self.conn, "http://example.com", "Duplicate description")
        self.assertIsNone(url_id)

    def test_invalid_url(self):
        self.assertFalse(is_valid_url("invalid-url"))
        self.assertTrue(is_valid_url("http://example.com"))

    def test_fetch_all_urls(self):
        add_url(self.conn, "http://example.com", "Example description")
        rows = fetch_all_urls(self.conn)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "http://example.com")
        self.assertEqual(rows[0][2], "Example description")
        self.assertFalse(rows[0][3])

    def test_update_url_status(self):
        url_id = add_url(self.conn, "http://example.com", "Example description")
        update_url_status(self.conn, url_id, True)
        rows = fetch_urls_by_status(self.conn, True)
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0][3])

    def test_fetch_urls_by_status_read(self):
        url_id_1 = add_url(self.conn, "http://example1.com", "Example description 1")
        url_id_2 = add_url(self.conn, "http://example2.com", "Example description 2")
        update_url_status(self.conn, url_id_1, True)
        rows = fetch_urls_by_status(self.conn, True)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "http://example1.com")

    def test_fetch_urls_by_status_unread(self):
        url_id_1 = add_url(self.conn, "http://example1.com", "Example description 1")
        url_id_2 = add_url(self.conn, "http://example2.com", "Example description 2")
        update_url_status(self.conn, url_id_1, True)
        rows = fetch_urls_by_status(self.conn, False)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "http://example2.com")

    def test_invalid_url_update(self):
        # Trying to update a URL ID that does not exist
        update_url_status(self.conn, 999, True)
        rows = fetch_urls_by_status(self.conn, True)
        self.assertEqual(len(rows), 0)
    
    def test_multiple_urls(self):
        add_url(self.conn, "http://example1.com", "Example description 1")
        add_url(self.conn, "http://example2.com", "Example description 2")
        add_url(self.conn, "http://example3.com", "Example description 3")
        rows = fetch_all_urls(self.conn)
        self.assertEqual(len(rows), 3)

    def test_delete_url(self):
        url_id = add_url(self.conn, "http://example.com", "Example description")
        delete_url(self.conn, url_id)
        rows = fetch_all_urls(self.conn)
        self.assertEqual(len(rows), 0)

if __name__ == '__main__':
    unittest.main()
