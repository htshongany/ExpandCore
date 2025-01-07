import configparser
import os

# Obtenir le chemin absolu du répertoire contenant ce fichier
base_path = os.path.dirname(os.path.abspath(__file__))

# Créer un objet ConfigParser
config = configparser.ConfigParser(allow_no_value=True)
config.read(os.path.join(base_path, 'config.ini'))

# Charger les variables
DATABASE = config['variables'].get('DATABASE', 'todos.db')
MAX_ATTEMPTS = int(config['variables'].get('MAX_ATTEMPTS', 3))
START_INDEX = int(config['variables'].get('START_INDEX', 0))

# Charger les modules sans clés explicites
MODULES = {str(i + START_INDEX): module for i, module in enumerate(config['modules']) if module is not None}
