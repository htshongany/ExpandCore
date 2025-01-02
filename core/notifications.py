# core/notifications.py

import os
import sys

class NotificationManager:
    def __init__(self):
        self.notifiers = []

    def register_notifier(self, notifier_func):
        """
        Registers a notifier function.

        Args:
            notifier_func (func): The notifier function to register.
        """
        try:
            self.notifiers.append(notifier_func)
        except Exception as e:
            print(f"Failed to register notifier: {e}")

    def send_notification(self, title, message):
        """
        Sends a notification using all registered notifiers.

        Args:
            title (str): The title of the notification.
            message (str): The message body of the notification.
        """
        for notifier in self.notifiers:
            try:
                notifier(title, message)
            except Exception as e:
                print(f"Failed to send notification: {e}")

notification_manager = NotificationManager()

if sys.platform == 'win32':
    from win10toast import ToastNotifier
    notifier = ToastNotifier()

    def windows_notifier(title, message):
        try:
            notifier.show_toast(title, message, duration=10)
        except Exception as e:
            print(f"Failed to show Windows notification: {e}")

    notification_manager.register_notifier(windows_notifier)
elif sys.platform == 'linux':
    import notify2
    try:
        notify2.init("Application Manager")
    except Exception as e:
        print(f"Failed to initialize Linux notifications: {e}")

    def linux_notifier(title, message):
        try:
            notification = notify2.Notification(title, message)
            notification.show()
        except Exception as e:
            print(f"Failed to show Linux notification: {e}")

    notification_manager.register_notifier(linux_notifier)
else:
    def fallback_notifier(title, message):
        try:
            print(f"Notification: {title} - {message}")
        except Exception as e:
            print(f"Failed to show fallback notification: {e}")

    notification_manager.register_notifier(fallback_notifier)

def send_notification(title, message):
    try:
        notification_manager.send_notification(title, message)
    except Exception as e:
        print(f"Failed to send notification: {e}")
