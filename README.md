# Projet de Ranking

## Description
Ce projet implémente un système de recherche d'information capable de lire une requête utilisateur, de tokeniser et transformer cette requête, de filtrer les documents correspondants dans un index, et d'appliquer une fonction de ranking pour ordonner ces documents. Le système supporte à la fois un ranking basé sur le nombre d'occurrences des mots-clés et le modèle BM25 pour une meilleure estimation de la pertinence.

## Installation

### Prérequis
- Python 3

### Structure des Données
Le projet utilise trois fichiers JSON pour stocker les données nécessaires :
- `title_pos_index.json` et `content_pos_index.json` pour l'indexation des titres et contenus des documents.
- `documents.json` contenant l'URL, l'ID et le titre de chaque document.

## Utilisation

Exécutez le fichier `main.py` pour démarrer le système de recherche avec une requête spécifique que vous pouvez modifier :
```bash
python main.py
```

## Fonctionnalités

- **Filtrage des Documents** : Filtre les documents en fonction des tokens présents dans les titres ou le contenu, avec une option pour choisir entre un filtrage de type ET ou OU.

- **Ranking des Documents** : Applique une fonction de ranking linéaire pour ordonner les documents filtrés, avec la possibilité d'utiliser un modèle de scoring basique ou le modèle BM25.

- **Prise en Compte des Stop Words** : Différencie les stop words des mots significatifs au moment du ranking pour améliorer la pertinence des résultats.

- **Exportation des Résultats** : Les résultats de la recherche sont exportés au format JSON, incluant le titre, l'URL, et le score de chaque document, ainsi que le nombre total de documents et le nombre de documents filtrés.

## Structure du Projet
- `data/input/` : Contient les fichiers JSON d'index et les documents.
- `data/output/` : Contient le fichier JSON des résultats de la recherche.
- `ranker/` : Contient le code pour le ranking des documents.
- `data/read.py` : Fonction pour charger les données depuis les fichiers JSON.
- `data/write.py` : Fonction pour enregistrer les résultats de recherche dans un fichier JSON.
- `main.py` : Point d'entrée pour démarrer le système de recherche.

## Auteur

Ce projet a été réalisé par Sven BARRAY dans le cadre d'un cours d'Indexation Web, lors de sa troisième année du cursus ingénieur à l'ENSAI