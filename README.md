# ExpandCore

Bienvenue dans Project Core, une application évolutive pour gérer des modules personnalisés. Ce projet a été conçu avec une architecture modulaire, ce qui permet d'ajouter facilement de nouveaux modules et de maintenir une évolutivité.

## Utilisation

Pour démarrer l'application, exécutez simplement le fichier `main.py` :

```bash
python main.py
```

Vous verrez un menu affiché avec les modules disponibles. Sélectionnez un module en entrant le numéro correspondant.

## Tests

Pour exécuter les tests unitaires, utilisez la commande suivante :

```bash
python -m unittest discover -s tests
```

Cette commande découvrira et exécutera tous les tests dans le répertoire `tests`.

## Créer un Nouveau Module

Pour créer un nouveau module, suivez les étapes ci-dessous :

1. Créez un nouveau répertoire dans le dossier `modules` avec le nom de votre module.
2. Ajoutez un fichier `__init__.py` dans ce répertoire. Ce fichier doit contenir au moins les informations d'identité du module (`name` et `version`) et une fonction `main` qui sera appelée lorsque le module sera sélectionné.

Exemple de structure pour un module nommé `example_module` :

```bash
modules/
└── example_module/
    └── __init__.py
```

Exemple de contenu pour `modules/example_module/__init__.py` :

```python
name = "Example Module"
version = "1.0.0"

def main():
    print("Example Module is running!")
```

3. Ajoutez le module à la configuration dans `config.py` :

```python
MODULES = {
    "0": "url_todo_list",
    "1": "example_module",
}
```

4. Exécutez l'application et sélectionnez votre nouveau module dans le menu.

## Contribution

Nous apprécions grandement toute contribution pour améliorer ce projet. Que vous soyez un développeur expérimenté ou débutant, toute aide est la bienvenue ! N'hésitez pas à soumettre des Pull Requests ou à ouvrir des Issues pour discuter des améliorations possibles.

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

Merci d'utiliser Project Core ! Si vous avez des questions ou des suggestions, n'hésitez pas à nous contacter.