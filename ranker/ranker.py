import re
import math

STOP_WORDS = set(['le', 'la', 'les', 'de', 'des', 'du', 'et', 'en', 'un', 'une', 'pour', 'dans', 'que', 'qui', 'sur', 'au', 'avec', 'ce', 'ces', 'par', 'se', 'comme', 'à', 'a', 'est'])
significant_word_weight = 1000  # Poids pour les tokens significatifs
stop_word_weight = 1  # Poids pour les stop words

def rank_documents(query, title_pos_index, content_pos_index, documents_data, filter_type='OR', bm25=True):
    """Calcule le score de ranking des documents, basé sur le nombre d'occurences des mots-clés de la requête"""
    tokens = preprocess_query(query)
    # Dans un soucis de performance, on travaille sur les documents dont les tokens sont dans le titre, mais le score se calcule sur le contenu.
    filtered_documents = filter_documents_by_title(tokens, title_pos_index, filter_type)

    n_docs = len(documents_data)
    filtered_documents_count = len(filtered_documents)
    avgdl = calculate_avgdl(documents_data)

    document_scores = {}
    for doc_id in filtered_documents:
        if bm25:
            score = bm25_score(doc_id, tokens, content_pos_index, documents_data, n_docs, avgdl)
        else:
            score = calculate_classic_score(tokens, doc_id, content_pos_index)
        document_scores[doc_id] = score

    # Trier les documents par leur score
    ranked_documents = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
    query_results = format_results(n_docs, filtered_documents_count, ranked_documents, documents_data)
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

def calculate_classic_score(tokens, doc_id, content_pos_index):
    """Calcule le score, basé sur le nombre simple d'occurences, en fonction tokens d'un document depuis son ID"""
    score = 0
    for token in tokens:
        if token in content_pos_index and str(doc_id) in content_pos_index[token]:
            weight = stop_word_weight if token in STOP_WORDS else significant_word_weight
            score += weight * content_pos_index[token][str(doc_id)]['count']
    return score

def bm25_score(doc_id, tokens, content_pos_index, documents_data, n_docs, avgdl, k1=1.5, b=0.75):
    """Calcule le score bm25"""
    doc_len = len(documents_data[int(doc_id)]["content"].split())
    score = 0
    for token in tokens:
        f = content_pos_index[token].get(str(doc_id), {}).get('count', 0)
        docs_with_token = len(content_pos_index.get(token, {}))
        idf_val = idf(n_docs, docs_with_token)
        weight = stop_word_weight if token in STOP_WORDS else significant_word_weight
        score += weight * idf_val * (f * (k1 + 1)) / (f + k1 * (1 - b + b * (doc_len / avgdl)))
    return score

def calculate_avgdl(documents_data):
    """Caclule la longueur moyenne des documents"""
    total_length = sum(len(doc["content"].split()) for doc in documents_data)
    return total_length / len(documents_data)

def idf(n_docs, docs_with_term):
    """Calcule l'Inverse Document Frequency de l'ensemble de nos documents"""
    return math.log((n_docs - docs_with_term + 0.5) / (docs_with_term + 0.5) + 1)