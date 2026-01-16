def build_arxiv_query(pools):
    """
    Build an arXiv query that requires:
    - at least one term from each pool (list of lists)
    in either the title or the abstract.

    pools: list of lists of strings
        Each inner list is a pool of terms.
    """

    def format_pool(pool):
        terms = []
        for term in pool:
            # Put quotes only if the term has spaces
            if " " in term:
                term = f'"{term}"'
            terms.append(term)
        # At least one term from this pool
        return " OR ".join(terms)

    # For each pool, build "(ti:(...) OR abs:(...))"
    pool_queries = []
    for pool in pools:
        formatted = format_pool(pool)
        pool_queries.append(f"(ti:({formatted}) OR abs:({formatted}))")

    # Join all pools with AND (require at least one term from each pool)
    query = " AND ".join(pool_queries)
    return query
