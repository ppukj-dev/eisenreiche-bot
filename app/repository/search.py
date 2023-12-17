from app.database import session_scope


def find_ik_entity(entity_class, search_term):
    with session_scope() as session:
        # Exact match query (case-insensitive)
        exact_match_result = session.query(entity_class).filter(
            entity_class.name.ilike(f'{search_term}')
        ).all()
    
        if exact_match_result:
            return exact_match_result
    
        # Similarity search query
        similarity_search_result = session.query(entity_class).filter(
            entity_class.name.ilike(f'%{search_term}%')
        ).limit(10).all()
    
        # Order results by relevancy (you might need to customize this based on your criteria)
        similarity_search_result = sorted(similarity_search_result,
                                          key=lambda x: x.name.lower().find(search_term.lower()))
    
        return similarity_search_result
