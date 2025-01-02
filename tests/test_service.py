# tests/core/test_service.py

import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
from core.service import ServiceManager

class TestServiceManager(unittest.TestCase):

    def setUp(self):
        self.service_manager = ServiceManager()

    @patch('builtins.open', new_callable=mock_open, read_data='1234')
    @patch('os.path.isfile', return_value=True)
    @patch('os.kill')
    def test_is_service_running(self, mock_kill, mock_isfile, mock_open):
        self.assertTrue(self.service_manager.is_service_running())
        mock_kill.side_effect = OSError
        self.assertFalse(self.service_manager.is_service_running())
        mock_isfile.return_value = False
        self.assertFalse(self.service_manager.is_service_running())

    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.Popen')
    @patch.object(ServiceManager, 'is_service_running', return_value=False)
    def test_start_service(self, mock_is_service_running, mock_popen, mock_open):
        mock_process = MagicMock()
        mock_process.pid = 1234
        mock_popen.return_value = mock_process
        
        self.service_manager.start_service()
        mock_popen.assert_called_once_with(['python', 'main.py'])
        mock_open.assert_called_once_with('service.pid', 'w')

    @patch('builtins.open', new_callable=mock_open, read_data='1234')
    @patch('os.path.isfile', return_value=True)
    @patch('os.kill')
    @patch('os.remove')
    def test_stop_service(self, mock_remove, mock_kill, mock_isfile, mock_open):
        self.service_manager.stop_service()
        mock_kill.assert_any_call(1234, 0)  # Check existence verification call
        mock_kill.assert_any_call(1234, 9)  # Check termination call
        mock_remove.assert_called_once_with('service.pid')

    @patch('time.sleep', return_value=None)
    @patch.object(ServiceManager, 'start_service')
    @patch.object(ServiceManager, 'stop_service')
    def test_restart_service(self, mock_stop_service, mock_start_service, mock_sleep):
        self.service_manager.restart_service()
        mock_stop_service.assert_called_once()
        mock_sleep.assert_called_once_with(1)
        mock_start_service.assert_called_once()

    @patch('core.service.ServiceManager.start_service')
    def test_register_module_start(self, mock_start_service):
        self.service_manager.register_module('url_todo_list', mock_start_service, MagicMock(), MagicMock())
        self.service_manager.start_module('url_todo_list')
        mock_start_service.assert_called_once()

    @patch('core.service.ServiceManager.stop_service')
    def test_register_module_stop(self, mock_stop_service):
        self.service_manager.register_module('url_todo_list', MagicMock(), mock_stop_service, MagicMock())
        self.service_manager.stop_module('url_todo_list')
        mock_stop_service.assert_called_once()

    @patch('core.service.ServiceManager.restart_service')
    def test_register_module_restart(self, mock_restart_service):
        self.service_manager.register_module('url_todo_list', MagicMock(), MagicMock(), mock_restart_service)
        self.service_manager.restart_module('url_todo_list')
        mock_restart_service.assert_called_once()

if __name__ == '__main__':
    unittest.main()
