from pathlib import Path
import pandas as pd
from pandas import DataFrame

from arxiv_query_to_dataframe import arxiv_query_to_dataframe
from plot_papers_per_year import plot_papers_per_year


if __name__ == "__main__":
    results_path: Path = Path('./results')
    results_path.mkdir(parents=True, exist_ok=True)
    xai_path = results_path / 'xai'
    xai_query = 'abs:("explainable AI" OR "interpretable AI" OR XAI OR "explainable artificial intelligence")'
    xai_data_path = xai_path / 'data.pkl'
    xai_papers_per_year_path = xai_path / 'papers_per_year.png'

    # xai_data = arxiv_query_to_dataframe(xai_query)
    # xai_data.to_pickle(xai_data_path)

    xai_data: DataFrame = pd.read_pickle(xai_data_path)
    print(xai_data.info())
    print(xai_data.head())

    plot_papers_per_year(
        df=xai_data,
        path=xai_papers_per_year_path,
    )

