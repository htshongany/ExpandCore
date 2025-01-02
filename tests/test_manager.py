import unittest
from unittest.mock import patch, MagicMock
from core.manager import ModuleManager

class TestModuleManager(unittest.TestCase):

    def setUp(self):
        self.manager = ModuleManager()

    @patch('importlib.import_module')
    def test_load_module(self, mock_import_module):
        mock_module = MagicMock()
        mock_module.name = "Mock Module"
        mock_module.version = "1.0.0"
        mock_import_module.return_value = mock_module
        self.manager.load_module("mock_module")
        self.assertIn("mock_module", self.manager.modules)

    def test_load_non_existent_module(self):
        with self.assertRaises(ImportError) as context:
            self.manager.load_module("non_existent_module")
        self.assertTrue("Failed to load module non_existent_module" in str(context.exception))

    @patch('importlib.import_module')
    def test_load_module_missing_identity(self, mock_import_module):
        mock_module = MagicMock()
        del mock_module.name
        mock_import_module.return_value = mock_module
        with self.assertRaises(ImportError) as context:
            self.manager.load_module("mock_module_missing_identity")
        self.assertTrue("Module mock_module_missing_identity is missing 'name' or 'version' information." in str(context.exception))

    @patch('importlib.import_module')
    def test_unload_module(self, mock_import_module):
        mock_module = MagicMock()
        mock_module.name = "Mock Module"
        mock_module.version = "1.0.0"
        mock_import_module.return_value = mock_module
        self.manager.load_module("mock_module")
        self.manager.unload_module("mock_module")
        self.assertNotIn("mock_module", self.manager.modules)

    @patch('importlib.import_module')
    def test_get_modules(self, mock_import_module):
        mock_module = MagicMock()
        mock_module.name = "Mock Module"
        mock_module.version = "1.0.0"
        mock_import_module.return_value = mock_module
        self.manager.load_module("mock_module")
        modules = self.manager.get_modules()
        self.assertIn("mock_module", modules)

if __name__ == '__main__':
    unittest.main()
