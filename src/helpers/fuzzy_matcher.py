from typing import Dict

from rapidfuzz import process, fuzz


class SimilarFinder:

    def search_similar_texts(
        source_text: str,
        db_texts: Dict[str, str],
        quantity: int = 5,
    ) -> list[tuple[str, str]]:

        results = process.extract(
            source_text,
            db_texts.keys(),
            scorer=fuzz.ratio,
            limit=quantity,
        )

        return [{match: db_texts[match]} for match, score, _ in results]
