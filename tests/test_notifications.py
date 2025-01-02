# tests/core/test_notifications.py

import unittest
from unittest.mock import patch
import sys
from core.notifications import notification_manager

class TestNotifications(unittest.TestCase):

    @unittest.skipIf(sys.platform != 'win32', "Skipping Windows test on non-Windows platform")
    @patch('core.notifications.ToastNotifier.show_toast')
    def test_send_notification_windows(self, mock_show_toast):
        notification_manager.send_notification("Test Title", "Test Message")
        mock_show_toast.assert_called_once_with("Test Title", "Test Message", duration=10)

    @unittest.skipIf(sys.platform == 'win32', "Skipping Linux test on Windows")
    @patch('core.notifications.notify2.Notification.show')
    def test_send_notification_linux(self, mock_show):
        notification_manager.send_notification("Test Title", "Test Message")
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()
