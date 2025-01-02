# core/service.py

import os
import subprocess
import time
from config import PID_FILE, SERVICE_NAME

class ServiceManager:
    def __init__(self):
        self.modules = {}

    def is_service_running(self):
        """
        Checks if the service is currently running by checking the PID file.

        Returns:
            bool: True if the service is running, False otherwise.
        """
        if os.path.isfile(PID_FILE):
            with open(PID_FILE, 'r') as pid_file:
                pid = int(pid_file.read().strip())
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                return False
        return False

    def start_service(self):
        """
        Starts the service if it is not already running.
        """
        if not self.is_service_running():
            try:
                process = subprocess.Popen(['python', 'main.py'])
                with open(PID_FILE, 'w') as pid_file:
                    pid_file.write(str(process.pid))
                print(f"Service {SERVICE_NAME} started successfully!")
            except Exception as e:
                print(f"Failed to start service: {e}")
        else:
            print(f"Service {SERVICE_NAME} is already running.")

    def stop_service(self):
        """
        Stops the service if it is currently running.
        """
        if self.is_service_running():
            try:
                with open(PID_FILE, 'r') as pid_file:
                    pid = int(pid_file.read().strip())
                os.kill(pid, 9)
                os.remove(PID_FILE)
                print(f"Service {SERVICE_NAME} stopped successfully!")
            except Exception as e:
                print(f"Failed to stop service: {e}")
        else:
            print(f"Service {SERVICE_NAME} is not running.")

    def restart_service(self):
        """
        Restarts the service by stopping it first, then starting it again after a short delay.
        """
        try:
            self.stop_service()
            time.sleep(1)
            self.start_service()
        except Exception as e:
            print(f"Failed to restart service: {e}")

    def register_module(self, module_name, start_func, stop_func, restart_func):
        """
        Registers a module with specific start, stop, and restart functions.

        Args:
            module_name (str): The name of the module.
            start_func (func): The function to start the module.
            stop_func (func): The function to stop the module.
            restart_func (func): The function to restart the module.
        """
        self.modules[module_name] = {
            "start": start_func,
            "stop": stop_func,
            "restart": restart_func
        }
    
    def start_module(self, module_name):
        if module_name in self.modules:
            try:
                self.modules[module_name]["start"]()
            except Exception as e:
                print(f"Failed to start module {module_name}: {e}")

    def stop_module(self, module_name):
        if module_name in self.modules:
            try:
                self.modules[module_name]["stop"]()
            except Exception as e:
                print(f"Failed to stop module {module_name}: {e}")

    def restart_module(self, module_name):
        if module_name in self.modules:
            try:
                self.modules[module_name]["restart"]()
            except Exception as e:
                print(f"Failed to restart module {module_name}: {e}")
