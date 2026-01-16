from pathlib import Path
import pandas as pd
from pandas import DataFrame

from arxiv_query_to_dataframe import arxiv_query_to_dataframe
from enrich_with_citations import enrich_with_citations
from plot_papers_per_year import plot_papers_per_year


def run_search(
    name: str,
    query: str,
    results_path: Path,
    force_download: bool = False,
) -> None:
    """
    Run a single arXiv search:
    - download papers if needed
    - load cached data
    - plot papers per year
    """
    search_path = results_path / name
    search_path.mkdir(parents=True, exist_ok=True)

    data_path = search_path / "data.csv"
    plot_path = search_path / "papers_per_year.png"

    if force_download or not data_path.exists():
        df = arxiv_query_to_dataframe(query)
        df = enrich_with_citations(df)
        # df.to_pickle(data_path)
        df.to_csv(data_path)
    else:
        # df: DataFrame = pd.read_pickle(data_path)
        df: DataFrame = pd.read_csv(data_path)

    print(f"\n=== {name.upper()} ===")
    print(df.info())
    print(df.head())

    plot_papers_per_year(
        df=df,
        path=plot_path,
    )
