import json

def save_results_to_file(filepath, data):
    """Enregistre les données fournies dans un fichier JSON."""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)