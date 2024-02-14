from ranker.ranker import rank_documents
from data.read import load_json_data
from data.write import save_results_to_file

if __name__ == "__main__":
    # Chemins vers les fichiers JSON
    title_index_path = 'data/input/title_pos_index.json'
    content_index_path = 'data/input/content_pos_index.json'
    documents_data_path = 'data/input/documents.json'

    # Chargement des données
    title_pos_index = load_json_data(title_index_path)
    content_pos_index = load_json_data(content_index_path)
    documents_data = load_json_data(documents_data_path)

    query = "le vaccin du covid"
    query_results = rank_documents(query, title_pos_index, content_pos_index, documents_data, filter_type="OR")

    # Sauvegarde des résultats
    output_path = 'data/output/results.json'
    save_results_to_file(output_path, query_results)

