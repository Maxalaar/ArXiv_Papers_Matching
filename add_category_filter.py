from typing import List

def add_category_filter(query: str, categories: List[str]) -> str:
    category_filter = "cat:(" + " OR ".join(categories) + ")"
    return f"({query}) AND {category_filter}"