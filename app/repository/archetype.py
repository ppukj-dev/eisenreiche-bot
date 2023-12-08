from app.model.archetype import Archetype, ArchetypeBenefit


class ArchetypeRepository:
    def __init__(self, database):
        self.db = database

    def find_ik_archetype(self, search_term):
        # Exact match query (case-insensitive)
        exact_match_result = self.db.query(Archetype).filter(Archetype.name.ilike(search_term)).all()

        if exact_match_result:
            return exact_match_result

        # Similarity search query
        similarity_search_result = self.db.query(Archetype).filter(
            Archetype.name.ilike(f'%{search_term}%')).limit(10).all()

        # Order results by relevancy (you might need to customize this based on your criteria)
        similarity_search_result = sorted(similarity_search_result,
                                          key=lambda x: x.name.lower().find(search_term.lower()))

        return similarity_search_result

    def find_ik_archetype_benefit(self, search_term):
        # Exact match query (case-insensitive)
        exact_match_result = self.db.query(ArchetypeBenefit).filter(ArchetypeBenefit.name.ilike(search_term)).all()

        if exact_match_result:
            return exact_match_result

        # Similarity search query
        similarity_search_result = self.db.query(ArchetypeBenefit).filter(
            ArchetypeBenefit.name.ilike(f'%{search_term}%')).limit(10).all()

        # Order results by relevancy (you might need to customize this based on your criteria)
        similarity_search_result = sorted(similarity_search_result,
                                          key=lambda x: x.name.lower().find(search_term.lower()))

        return similarity_search_result
