import arxiv
import matplotlib.pyplot as plt
import os
from collections import Counter
from datetime import datetime


def ensure_results_directory():
    """Create results directory if it doesn't exist."""
    if not os.path.exists("results"):
        os.makedirs("results")
        print("Created 'results' directory")


def count_papers_by_year(topic_name, search_query, max_results=5000):
    """
    Count papers by year for a given arXiv search query and collect paper details.

    Args:
        topic_name (str): Display name for the topic
        search_query (str): arXiv search query string
        max_results (int): Maximum number of papers to retrieve

    Returns:
        tuple: (yearly_counts, papers_list) where yearly_counts is dict Year->count,
               and papers_list is list of dicts with paper details
    """
    print(f"\nSearching for {topic_name} papers...")
    print(f"Query: {search_query}")

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

    yearly_counts = Counter()
    papers_list = []  # List to store paper details
    total_processed = 0

    try:
        # Client.results() returns a generator
        for result in client.results(search):
            # Extract year from published date
            if result.published:
                year = result.published.year
                yearly_counts[year] += 1
                total_processed += 1

                # Store paper details
                paper_info = {
                    'title': result.title,
                    'url': result.entry_id,
                    'year': year,
                    'authors': [author.name for author in result.authors],
                    'summary': result.summary,
                    'published': result.published.isoformat(),
                    'categories': result.categories
                }
                papers_list.append(paper_info)

            # Progress indicator for large result sets
            if total_processed % 500 == 0:
                print(f"  Processed {total_processed} papers...")

    except Exception as e:
        print(f"Error during search: {e}")

    print(f"Total {topic_name} papers processed: {total_processed}")

    # Convert to regular dict and sort by year
    return dict(sorted(yearly_counts.items())), papers_list


def create_comparison_chart(xai_counts, xrl_counts):
    """
    Create a comparative bar chart for XAI and XRL publication trends.
    Saves chart to results directory.

    Args:
        xai_counts (dict): XAI yearly counts
        xrl_counts (dict): XRL yearly counts
    """
    # Prepare data for plotting
    all_years = sorted(set(list(xai_counts.keys()) + list(xrl_counts.keys())))

    # Skip years before 2000 (unlikely to have relevant papers)
    all_years = [year for year in all_years if year >= 2000]

    if not all_years:
        print("No data to plot.")
        return None, None

    # Get counts for each year
    xai_values = [xai_counts.get(year, 0) for year in all_years]
    xrl_values = [xrl_counts.get(year, 0) for year in all_years]

    # Calculate statistics for annotation
    total_xai = sum(xai_values)
    total_xrl = sum(xrl_values)
    xrl_percentage = (total_xrl / total_xai * 100) if total_xai > 0 else 0

    # Create visualization
    fig, ax = plt.subplots(figsize=(14, 8))

    # Bar positions and width
    x = range(len(all_years))
    width = 0.35

    # Create grouped bars
    bars_xai = ax.bar(
        [pos - width / 2 for pos in x], xai_values, width,
        label=f'Explainable AI (XAI) - Total: {total_xai:,}',
        color='steelblue', alpha=0.8, edgecolor='black'
    )

    bars_xrl = ax.bar(
        [pos + width / 2 for pos in x], xrl_values, width,
        label=f'Explainable RL (XRL) - Total: {total_xrl:,}',
        color='coral', alpha=0.8, edgecolor='black'
    )

    # Customize chart
    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Papers', fontsize=14, fontweight='bold')
    ax.set_title(
        'arXiv Publication Trends: Explainable AI vs Explainable Reinforcement Learning\n'
        f'XRL represents {xrl_percentage:.1f}% of XAI publications',
        fontsize=16, fontweight='bold', pad=20
    )

    ax.set_xticks(x)
    ax.set_xticklabels(all_years, rotation=45, ha='right')
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')

    # Add value labels on top of bars
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.annotate(
                    f'{height:,}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords='offset points',
                    ha='center', va='bottom',
                    fontsize=9, fontweight='bold'
                )

    add_value_labels(bars_xai)
    add_value_labels(bars_xrl)

    # Add annotation about data source
    current_year = datetime.now().year
    plt.figtext(
        0.02, 0.02,
        f"Data source: arXiv API via arxiv.py | Retrieved: {current_year}\n"
        "Note: Counts based on paper titles, abstracts, and keywords matching search terms",
        fontsize=9, style='italic', alpha=0.7
    )

    plt.tight_layout()

    # Save to results directory
    output_file = os.path.join("results", "xai_vs_xrl_trends.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nChart saved as '{output_file}'")

    return fig, ax


def save_papers_to_csv(papers_list, topic_name):
    """
    Save paper details to a CSV file in results directory.

    Args:
        papers_list (list): List of paper dictionaries
        topic_name (str): Name of the topic for filename
    """
    if not papers_list:
        print(f"No papers to save for {topic_name}")
        return

    # Create safe filename from topic name
    safe_topic = "".join(c if c.isalnum() else "_" for c in topic_name)
    filename = os.path.join("results", f"{safe_topic}_papers.csv")

    with open(filename, 'w', encoding='utf-8') as f:
        # Write header
        f.write("Title,URL,Year,Authors,Published,Categories\n")

        # Write paper details
        for paper in papers_list:
            # Escape quotes in title and clean up
            title = paper['title'].replace('"', '""')
            url = paper['url']
            year = paper['year']

            # Format authors as semicolon-separated list
            authors = ";".join(paper['authors']).replace('"', '""')
            published = paper['published']
            categories = ";".join(paper['categories'])

            # Write CSV line
            f.write(f'"{title}","{url}",{year},"{authors}","{published}","{categories}"\n')

    print(f"Saved {len(papers_list)} {topic_name} papers to '{filename}'")


def save_results_to_csv(xai_counts, xrl_counts):
    """
    Save yearly counts to a CSV file in results directory.

    Args:
        xai_counts (dict): XAI yearly counts
        xrl_counts (dict): XRL yearly counts
    """
    all_years = sorted(set(list(xai_counts.keys()) + list(xrl_counts.keys())))
    all_years = [year for year in all_years if year >= 2000]

    filename = os.path.join("results", "xai_xrl_yearly_counts.csv")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Year,XAI_Papers,XRL_Papers,Total_Papers,XRL_Percentage\n")

        for year in all_years:
            xai = xai_counts.get(year, 0)
            xrl = xrl_counts.get(year, 0)
            total = xai + xrl
            percentage = (xrl / xai * 100) if xai > 0 else 0

            f.write(f"{year},{xai},{xrl},{total},{percentage:.1f}\n")

    print(f"Yearly counts saved to '{filename}'")


def main():
    """
    Main function to execute the arXiv analysis.
    """
    print("=" * 70)
    print("arXiv Research Trends: XAI vs XRL")
    print("Using arxiv.py Python package")
    print("=" * 70)

    # Ensure results directory exists
    ensure_results_directory()

    # Define search queries using arXiv query syntax
    xai_query = 'abs:("explainable AI" OR "interpretable AI" OR XAI OR "explainable artificial intelligence")'
    xrl_query = 'abs:("explainable reinforcement learning" OR "interpretable reinforcement learning" OR XRL OR "explainable RL")'

    # Get yearly counts and paper details
    print("\n" + "=" * 70)
    xai_counts, xai_papers = count_papers_by_year(
        "Explainable AI (XAI)",
        xai_query,
        max_results=10000
    )

    print("\n" + "=" * 70)
    xrl_counts, xrl_papers = count_papers_by_year(
        "Explainable Reinforcement Learning (XRL)",
        xrl_query,
        max_results=5000
    )

    # Display summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    if xai_counts:
        years = list(xai_counts.keys())
        print(f"XAI year range: {min(years)} to {max(years)}")
        print(f"XAI total papers: {sum(xai_counts.values()):,}")

    if xrl_counts:
        years = list(xrl_counts.keys())
        print(f"XRL year range: {min(years)} to {max(years)}")
        print(f"XRL total papers: {sum(xrl_counts.values()):,}")

    # Save paper details to CSV
    print("\n" + "=" * 70)
    print("SAVING PAPER DETAILS")
    print("=" * 70)

    save_papers_to_csv(xai_papers, "XAI")
    save_papers_to_csv(xrl_papers, "XRL")

    # Save yearly counts
    save_results_to_csv(xai_counts, xrl_counts)

    # Create and save visualization
    print("\n" + "=" * 70)
    print("CREATING VISUALIZATION")
    print("=" * 70)

    fig, ax = create_comparison_chart(xai_counts, xrl_counts)

    # Show the plot if we have one
    if fig:
        plt.show()

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print("All results saved in the 'results' directory:")
    print(f"  - xai_vs_xrl_trends.png (chart)")
    print(f"  - xai_xrl_yearly_counts.csv (yearly statistics)")
    print(f"  - XAI_papers.csv (detailed XAI paper list)")
    print(f"  - XRL_papers.csv (detailed XRL paper list)")
    print("=" * 70)


if __name__ == "__main__":
    main()