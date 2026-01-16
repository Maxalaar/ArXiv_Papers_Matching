import arxiv
import pandas as pd
import re
import time
from typing import Optional


def extract_arxiv_id(arxiv_url: str) -> Optional[str]:
    """
    Extract the arXiv id (without version suffix) from an arXiv URL like:
    https://arxiv.org/abs/2301.12345v2 -> 2301.12345
    """
    if not arxiv_url:
        return None
    m = re.search(r"arxiv\.org/abs/([^v/]+)", arxiv_url)
    return m.group(1) if m else None


def arxiv_query_to_dataframe(search_query, max_results=None):
    """
    Collect papers from arXiv and save to pandas DataFrame.

    Args:
        search_query (str): arXiv search query string
        max_results (int): Maximum number of papers to retrieve

    Returns:
        pd.DataFrame: DataFrame containing paper details
    """
    print(f"Query: {search_query}")
    print(f"Collecting papers from arXiv...")

    # Configure client with polite delays
    client = arxiv.Client(
        page_size=100,
        delay_seconds=3.0,
        num_retries=5
    )

    # Create search object
    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    papers_data = []
    total_processed = 0
    start_time = time.time()

    try:
        # Client.results() returns a generator
        for result in client.results(search):
            if result.published:
                # Extract paper details
                paper_info = {
                    'title': result.title,
                    'url': result.entry_id,
                    "arxiv_id": extract_arxiv_id(result.entry_id),
                    'doi': result.doi,
                    'year': result.published.year,
                    'month': result.published.month,
                    'published_date': result.published,
                    'authors': [author.name for author in result.authors],
                    'summary': result.summary,
                    'categories': result.categories,
                    'primary_category': result.primary_category,
                    'updated': result.updated if hasattr(result, 'updated') else None,
                }
                papers_data.append(paper_info)
                total_processed += 1

            # Progress indicator
            if total_processed % 100 == 0:
                elapsed = time.time() - start_time
                print(f"  Collected {total_processed} papers... ({elapsed:.1f}s)")

    except Exception as e:
        print(f"Error during collection: {e}")
        # Save what we have so far
        if papers_data:
            print(f"  Saving {len(papers_data)} collected papers...")

    # Create DataFrame
    df = pd.DataFrame(papers_data)

    elapsed_total = time.time() - start_time
    print(f"Total papers collected: {len(df):,} (in {elapsed_total:.1f}s)")

    return df