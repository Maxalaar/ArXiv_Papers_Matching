from pathlib import Path
import pandas as pd
from pandas import DataFrame

from arxiv_query_to_dataframe import arxiv_query_to_dataframe
from plot_papers_per_year import plot_papers_per_year
from run_search import run_search


# CATEGORIES = [
#     "cs.AI", "cs.LG", "cs.CL", "cs.HC",
#     "math.ST", "math.OC",
#     "stat.ML",
# ]

CATEGORIES = [
    "cs.*",
    "math.*",
    "stat.*",
]

CATEGORY_FILTER = "cat:(" + " OR ".join(CATEGORIES) + ")"


SEARCHES = {
    # "xai": {
    #     "query": (
    #         'abs:("explainable artificial intelligence" '
    #         'OR "interpretable artificial intelligence" '
    #         'OR "explainable AI" '
    #         'OR "interpretable AI" '
    #         'OR "XAI")'
    #     )
    # },

    "xrl": {
        "query": (
            'abs:("explainable reinforcement learning" '
            'OR "interpretable reinforcement learning" '
            'OR "explainable RL" '
            'OR "interpretable RL" '
            'OR "XRL")'
        )
    },

    # "rl": {
    #     "query": (
    #         'abs:("reinforcement learning" '
    #         'OR "RL")'
    #     )
    # },
    #
    # "llm": {
    #     "query": (
    #         'abs:("large language model" '
    #         'OR "LLM")'
    #     )
    # },
}



def add_category_filter(query: str) -> str:
    return f"({query}) AND {CATEGORY_FILTER}"


if __name__ == "__main__":
    results_path = Path("./results")
    results_path.mkdir(exist_ok=True)

    for name, config in SEARCHES.items():
        full_query = add_category_filter(config["query"])

        run_search(
            name=name,
            query=full_query,
            results_path=results_path,
            force_download=False,
        )


