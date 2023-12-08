from app.model.spell import Spell


class SpellRepository:
    def __init__(self, database):
        self.db = database

    def find_ik_spell(self, search_term):
        # Exact match query (case-insensitive)
        exact_match_result = self.db.query(Spell).filter(Spell.name.ilike(search_term)).all()

        if exact_match_result:
            return exact_match_result

        # Similarity search query
        similarity_search_result = self.db.query(Spell).filter(
            Spell.name.ilike(f'%{search_term}%')).limit(10).all()

        # Order results by relevancy (you might need to customize this based on your criteria)
        similarity_search_result = sorted(similarity_search_result,
                                          key=lambda x: x.name.lower().find(search_term.lower()))

        return similarity_search_result
