from typing import Optional
import pandas as pd
from semanticscholar import SemanticScholar

def enrich_with_citations(df: pd.DataFrame, api_key: Optional[str] = 'S90a8eGZ46hIZXRVyNNT17HKXI3kiiE5nrjxMG5b') -> pd.DataFrame:
    """
    Enrich DataFrame with citation info from Semantic Scholar.

    Adds columns:
        - citation_count
        - citations_titles
        - citations_authors
        - citations_years
    """
    sch = SemanticScholar(api_key=api_key) if api_key else SemanticScholar()
    df = df.copy()

    citation_counts = []
    citations_titles = []
    citations_authors = []
    citations_years = []

    for idx, row in df.iterrows():
        arxiv_id = row.get("arxiv_id")
        paper_id = f"arXiv:{arxiv_id}"

        try:
            paper = sch.get_paper(
                paper_id,
                fields=[
                    "title",
                    "citationCount",
                    "citations.authors",
                    "citations.title",
                    "citations.year",
                    "citations.paperId",
                ],
            )

            print('name: ' + str(paper.title))
            print('citation count: ' + str(paper.citationCount))
            print()

            citation_counts.append(paper.citationCount)
            citations_titles.append([c.title for c in paper.citations])
            citations_authors.append([[a.name for a in c.authors] for c in paper.citations])
            citations_years.append([c.year for c in paper.citations])

        except Exception as e:
            print(f"[warning] failed to fetch data for {paper_id}: {e}")
            citation_counts.append(None)
            citations_titles.append(None)
            citations_authors.append(None)
            citations_years.append(None)

    df["citation_count"] = citation_counts
    df["citations_titles"] = citations_titles
    df["citations_authors"] = citations_authors
    df["citations_years"] = citations_years

    return df
