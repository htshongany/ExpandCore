import configparser

# Créer un objet ConfigParser
config = configparser.ConfigParser()

# Lire le fichier de configuration
config.read('config.ini')

# Charger les variables
DATABASE = config['variables'].get('DATABASE', 'todos.db')
PID_FILE = config['variables'].get('PID_FILE', 'service.pid')
SERVICE_NAME = config['variables'].get('SERVICE_NAME', 'UrlTodoListService')

# Charger les modules
MODULES = {str(i): module for i, (key, module) in enumerate(config['modules'].items())}
