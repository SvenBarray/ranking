import re

def rank_documents(query, title_pos_index, content_pos_index, documents_data):
    """Calcule le score de ranking des documents, basé sur le nombre d'occurences des mots-clés de la requête"""
    tokens = preprocess_query(query)
    # Dans un soucis de performance, on travaille sur les documents dont les tokens sont dans le titre, mais le score se calcule sur le contenu.
    filtered_documents = filter_documents_by_title(tokens, title_pos_index)
    total_documents = len(documents_data)
    filtered_documents_count = len(filtered_documents)

    document_scores = {}
    for doc_id in filtered_documents:
        # Calculer le score du contenu
        score = 0
        for token in tokens:
            if token in content_pos_index and str(doc_id) in content_pos_index[token]:
                score += content_pos_index[token][str(doc_id)]['count']
        document_scores[doc_id] = score

    # Trier les documents par leur score
    ranked_documents = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
    query_results = format_results(total_documents, filtered_documents_count, ranked_documents, documents_data)
    return query_results

def preprocess_query(query):
    """Met les éléments de la requête en minuscule, retire la ponctuation, et les tokénise"""
    query = query.lower()
    query = re.sub(r"[^\w\s']", '', query)
    tokens = query.split()
    return tokens

def filter_documents_by_title(tokens, title_pos_index):
    """Filtre les documents contenant tous les tokens de la requête"""
    documents_with_all_tokens = set()
    # Initialisation avec les documents contenant le premier token
    if tokens:
        documents_with_all_tokens = set(title_pos_index.get(tokens[0], []))
        for token in tokens[1:]:
            documents_with_all_tokens &= set(title_pos_index.get(token, []))
    return list(documents_with_all_tokens)

def get_title_and_url_from_id(doc_id, documents_data):
    """Récupération du tutre et de l'url de la page depuis sont id"""
    doc_info = documents_data[int(doc_id)]
    return doc_info.get('title', ''), doc_info.get('url', '')

def format_results(total_documents, filtered_documents_count, ranked_documents, documents_data):
    """Construction de la structure de données pour les résultats"""
    results_data = {
        "total_documents": total_documents,
        "filtered_documents_count": filtered_documents_count,
        "results": []
    }
    for doc_id, score in ranked_documents:
        title, url = get_title_and_url_from_id(doc_id, documents_data)
        results_data["results"].append({
            "title": title,
            "url": url,
            "score": score
        })
    return results_data