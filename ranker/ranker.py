import re

STOP_WORDS = set(['le', 'la', 'les', 'de', 'des', 'du', 'et', 'en', 'un', 'une', 'pour', 'dans', 'que', 'qui', 'sur', 'au', 'avec', 'ce', 'ces', 'par', 'se', 'comme', 'à', 'a', 'est'])


def rank_documents(query, title_pos_index, content_pos_index, documents_data, filter_type='AND'):
    """Calcule le score de ranking des documents, basé sur le nombre d'occurences des mots-clés de la requête"""
    tokens = preprocess_query(query)
    # Dans un soucis de performance, on travaille sur les documents dont les tokens sont dans le titre, mais le score se calcule sur le contenu.
    filtered_documents = filter_documents_by_title(tokens, title_pos_index, filter_type)
    total_documents = len(documents_data)
    filtered_documents_count = len(filtered_documents)

    document_scores = {}
    for doc_id in filtered_documents:
        score = calculate_score(tokens, doc_id, content_pos_index)
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

def filter_documents_by_title(tokens, title_pos_index, filter_type='AND'):
    """Filtre les documents basé sur les tokens de la requête avec un filtre de type ET ou OU."""
    all_documents = set()
    documents_with_any_token = set()

    for token in tokens:
        documents_with_token = set(title_pos_index.get(token, {}).keys())
        if filter_type.upper() == 'AND':
            if not all_documents:
                all_documents = documents_with_token
            else:
                all_documents &= documents_with_token
        else:  # Pour le filtre OU
            documents_with_any_token |= documents_with_token

    return list(all_documents if filter_type.upper() == 'AND' else documents_with_any_token)

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

def calculate_score(tokens, doc_id, content_pos_index):
    """Calcule le score en fonction tokens d'un document depuis son ID"""
    score = 0
    significant_weight = 1000  # Poids pour les tokens significatifs
    stop_word_weight = 1  # Poids pour les stop words

    for token in tokens:
        if token in content_pos_index and str(doc_id) in content_pos_index[token]:
            # Appliquer un poids différent si le token est un stop word ou non
            weight = stop_word_weight if token in STOP_WORDS else significant_weight
            score += weight * content_pos_index[token][str(doc_id)]['count']
    
    return score