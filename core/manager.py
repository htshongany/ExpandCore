import importlib

class ModuleManager:
    """
    ModuleManager class to manage loading, unloading, and handling of modules.

    Attributes:
        modules (dict): Dictionary containing loaded modules.

    Methods:
        load_module(module_name):
            Loads a module by its name.

        unload_module(module_name):
            Unloads a module by its name.

        get_modules():
            Returns a list of loaded module names.
    """

    def __init__(self):
        """
        Initializes a new ModuleManager object with an empty dictionary for modules.
        """
        self.modules = {}

    def load_module(self, module_name):
        """
        Loads a module by its name and adds it to the loaded modules dictionary.

        Args:
            module_name (str): The name of the module to load.

        Raises:
            ImportError: If the module cannot be imported or if identity information is missing.
        """
        try:
            module = importlib.import_module(f"modules.{module_name}")
            if not hasattr(module, "name") or not hasattr(module, "version"):
                raise ImportError(f"Module {module_name} is missing 'name' or 'version' information.")
            self.modules[module_name] = module
            print(f"Module {module_name} loaded successfully! Name: {module.name}, Version: {module.version}")
        except ImportError as e:
            print(f"Error: Failed to load module '{module_name}': {e}. Please ensure the module exists and has 'name' and 'version' attributes.")
            raise ImportError(f"Failed to load module {module_name}: {e}")

    def unload_module(self, module_name):
        """
        Unloads a module by its name and removes it from the loaded modules dictionary.

        Args:
            module_name (str): The name of the module to unload.
        """
        if module_name in self.modules:
            try:
                del self.modules[module_name]
                print(f"Module {module_name} unloaded successfully!")
            except KeyError as e:
                print(f"Failed to unload module {module_name}: {e}")

    def get_modules(self):
        """
        Returns a list of currently loaded module names.

        Returns:
            list: A list of loaded module names.
        """
        return list(self.modules.keys())
