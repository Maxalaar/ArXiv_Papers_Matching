from pathlib import Path

from run_search import run_search

CATEGORIES = [
    "cs.*",
    "math.*",
    "stat.*",
]

SEARCHES = {
    "xrl": {
        "categories": CATEGORIES,
        "pools": [
            [
                "reinforcement learning",
                "RL",
            ],
            [
                "explainable",
                "explainability",
                "interpretable",
                "interpretability",
                "understandable",
            ]
        ]
    }
}

if __name__ == "__main__":
    results_path = Path("./results")
    results_path.mkdir(exist_ok=True)

    for name, config in SEARCHES.items():
        run_search(
            name=name,
            categories=config['categories'],
            pools=config['pools'],
            results_path=results_path,
            force_download=True,
            # max_results=200,
            use_citations=True,
        )
