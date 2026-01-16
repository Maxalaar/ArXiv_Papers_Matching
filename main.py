from pathlib import Path

from run_search import run_search


CATEGORIES = [
    "cs.*",
    "math.*",
    "stat.*",
]

CATEGORY_FILTER = "cat:(" + " OR ".join(CATEGORIES) + ")"


SEARCHES = {
    "xrl": {
        "query": (
            'abs:("explainable reinforcement learning" '
            'OR "interpretable reinforcement learning" '
            'OR "explainable RL" '
            'OR "interpretable RL" '
            'OR "XRL")'
        )
    },
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
            force_download=True,
        )


