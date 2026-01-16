from pathlib import Path
from typing import List, Optional

import pandas as pd
from pandas import DataFrame

from add_category_filter import add_category_filter
from arxiv_query_to_dataframe import arxiv_query_to_dataframe
from build_arxiv_query import build_arxiv_query
from enrich_with_citations import enrich_with_citations
from filter_dataframe_by_pools import filter_dataframe_by_pools
from plot_papers_per_year import plot_papers_per_year


def run_search(
    name: str,
    categories: List[str],
    pools: List[List[str]],
    results_path: Path,
    force_download: bool = False,
    max_results: Optional[int] = None,
    use_citations: bool = True,
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
        query = build_arxiv_query(pools)
        query = add_category_filter(query, categories)
        df = arxiv_query_to_dataframe(query, max_results)
        df = filter_dataframe_by_pools(df, pools)
        if use_citations:
            df = enrich_with_citations(df)
        df.to_csv(data_path)
    else:
        df: DataFrame = pd.read_csv(data_path)

    print(f"\n=== {name.upper()} ===")
    print(df.info())
    print(df.head())

    plot_papers_per_year(
        df=df,
        path=plot_path,
    )
