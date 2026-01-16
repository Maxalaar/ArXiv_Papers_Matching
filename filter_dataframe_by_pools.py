import pandas as pd
import re

def filter_dataframe_by_pools(df: pd.DataFrame, pools: list[list[str]]) -> pd.DataFrame:
    """
    Filter a DataFrame of arXiv papers so that only rows with at least one match
    from each pool in either the title or the summary are kept.
    Each keyword (even multi-word like "reinforcement learning") must match as a whole.

    Args:
        df (pd.DataFrame): DataFrame with columns 'title' and 'summary'
        pools (list of lists): Each inner list is a pool of keywords. At least one
                               keyword from each pool must appear as a separate term
                               in title or summary.

    Returns:
        pd.DataFrame: Filtered DataFrame
    """

    if df.empty:
        return df

    # Precompute regex patterns for each pool
    pool_patterns = []
    for pool in pools:
        escaped_terms = []
        for term in pool:
            # Escape regex chars
            term_escaped = re.escape(term)
            # Replace escaped spaces with \s+ to match multi-word terms
            term_escaped = term_escaped.replace(r'\ ', r'\s+')
            # Add word boundaries
            escaped_terms.append(r'\b' + term_escaped + r'\b')
        # Join with OR for this pool
        pattern = '(' + '|'.join(escaped_terms) + ')'
        pool_patterns.append(re.compile(pattern, re.IGNORECASE))

    def row_matches(row):
        text = f"{row['title']} {row['summary']}"
        return all(pattern.search(text) for pattern in pool_patterns)

    # Apply row_matches to each row
    mask = df.apply(row_matches, axis=1)
    filtered_df = df[mask].reset_index(drop=True)
    return filtered_df
