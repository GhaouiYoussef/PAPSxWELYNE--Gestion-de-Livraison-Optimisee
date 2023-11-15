# Gestion de la Livraison - PAPSxWELYNE

Ce projet est dédié à la gestion optimisée de la livraison de marchandises en utilisant des algorithmes de routage. Il fournit une solution pour optimiser les itinéraires de livraison pour plusieurs missions et tâches.

## Description des Fichiers

- `Final_algorithm.py` contient la fonction principale qui génère les itinéraires de livraison optimisés.
- `Main_functions.py` contient les fonctions secondaires utilisées pour les calculs d'optimisation et autres .
- `TSP_modified.py` contient les fonctions primaires utilisées pour les calculs d'optimisation.
- `API_Call.py` est un fichier essentiel pour l'API de l'application.

## Exécution en Local

Si vous souhaitez exécuter cette application en local pour des tests ou des développements, suivez ces étapes :

1. Assurez-vous d'avoir Python installé sur votre système. Si ce n'est pas le cas, téléchargez-le à partir de [Python.org](https://www.python.org/downloads/) et installez-le.

2. Clonez ce référentiel sur votre machine en utilisant la commande suivante :

   ```bash
   git clone https://github.com/GhaouiYoussef/PAPSxWELYNE--Gestion-de-Livraison-Optimisee/
   ```

3. Accédez au répertoire de votre projet :

   ```bash
   cd 19-10-2023
   ```


4. Installez les dépendances requises à partir du fichier `requirements.txt` :

   ```bash
   pip install -r requirements.txt
   ```


5. Maintenant, vous pouvez exécuter l'application en utilisant la commande suivante :

   ```bash
   python API_Call.py
   ```

6. Si il y un problem dans l'execution(Puis reessayer 5. ) :

   ```bash
   pip install --upgrade Flask
   ```

   L'application devrait être accessible à l'adresse [http://localhost:5000](http://localhost:5000). Vous pouvez accéder à l'API à l'aide de cet URL.

N'oubliez pas que vous devrez également obtenir des clés d'API si vous utilisez des services tiers, comme Google Maps, pour des fonctionnalités spécifiques de l'application.

## Test avec Postman

Si vous souhaitez tester l'API en local, vous pouvez utiliser des outils comme Postman pour envoyer des demandes POST aux points d'extrémité appropriés. Des exemples de données de missions sont fournis dans le fichier `missions.js`.

## À Propos du Projet

Ce projet vise à fournir une solution efficace pour la gestion de la livraison de marchandises en optimisant les itinéraires. Il utilise des algorithmes avancés pour s'assurer que les missions sont accomplies de la manière la plus efficace possible.

**Auteur** : Youssef Ghaoui
