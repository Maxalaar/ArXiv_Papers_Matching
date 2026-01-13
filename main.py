import arxiv
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime


def count_papers_by_year(topic_name, search_query, max_results=5000):
    """
    Count papers by year for a given arXiv search query.

    Args:
        topic_name (str): Display name for the topic
        search_query (str): arXiv search query string
        max_results (int): Maximum number of papers to retrieve

    Returns:
        dict: Year -> count mapping
    """
    print(f"\nSearching for {topic_name} papers...")
    print(f"Query: {search_query}")

    # Configure client with polite delays (arXiv recommends 3 seconds)[citation:2]
    client = arxiv.Client(
        page_size=100,  # Results per API request
        delay_seconds=3.0,  # Polite delay between requests
        num_retries=5  # Retry failed requests
    )

    # Create search object
    # Sort by submission date to get chronological results[citation:8]
    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    yearly_counts = Counter()
    total_processed = 0

    try:
        # Client.results() returns a generator[citation:1]
        for result in client.results(search):
            # Extract year from published date
            if result.published:
                year = result.published.year
                yearly_counts[year] += 1
                total_processed += 1

            # Progress indicator for large result sets
            if total_processed % 500 == 0:
                print(f"  Processed {total_processed} papers...")

    except Exception as e:
        print(f"Error during search: {e}")

    print(f"Total {topic_name} papers processed: {total_processed}")

    # Convert to regular dict and sort by year
    return dict(sorted(yearly_counts.items()))


def create_comparison_chart(xai_counts, xrl_counts, output_file="xai_vs_xrl_trends.png"):
    """
    Create a comparative bar chart for XAI and XRL publication trends.

    Args:
        xai_counts (dict): XAI yearly counts
        xrl_counts (dict): XRL yearly counts
        output_file (str): Name for output chart file
    """
    # Prepare data for plotting
    all_years = sorted(set(list(xai_counts.keys()) + list(xrl_counts.keys())))

    # Skip years before 2000 (unlikely to have relevant papers)
    all_years = [year for year in all_years if year >= 2000]

    if not all_years:
        print("No data to plot.")
        return

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

    # Save and show
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nChart saved as '{output_file}'")
    plt.show()

    return fig, ax


def save_results_to_csv(xai_counts, xrl_counts, filename="xai_xrl_analysis.csv"):
    """
    Save yearly counts to a CSV file for further analysis.

    Args:
        xai_counts (dict): XAI yearly counts
        xrl_counts (dict): XRL yearly counts
        filename (str): Output CSV filename
    """
    all_years = sorted(set(list(xai_counts.keys()) + list(xrl_counts.keys())))
    all_years = [year for year in all_years if year >= 2000]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Year,XAI_Papers,XRL_Papers,Total_Papers,XRL_Percentage\n")

        for year in all_years:
            xai = xai_counts.get(year, 0)
            xrl = xrl_counts.get(year, 0)
            total = xai + xrl
            percentage = (xrl / xai * 100) if xai > 0 else 0

            f.write(f"{year},{xai},{xrl},{total},{percentage:.1f}\n")

    print(f"Data saved to '{filename}'")


if __name__ == "__main__":
    """
    Main function to execute the arXiv analysis.
    """
    print("=" * 70)
    print("arXiv Research Trends: XAI vs XRL")
    print("Using arxiv.py Python package")
    print("=" * 70)

    # Define search queries using arXiv query syntax[citation:7]
    # Search in titles, abstracts, and comments
    xai_query = 'abs:("explainable AI" OR "interpretable AI" OR XAI OR "explainable artificial intelligence")'
    xrl_query = 'abs:("explainable reinforcement learning" OR "interpretable reinforcement learning" OR XRL OR "explainable RL")'

    # You can also search specific fields[citation:7]:
    # xai_query = 'ti:"explainable AI" OR abs:"interpretable AI" OR all:XAI'
    # xrl_query = 'ti:"explainable reinforcement learning" OR abs:XRL'

    # Get yearly counts
    print("\n" + "=" * 70)
    xai_counts = count_papers_by_year(
        "Explainable AI (XAI)",
        xai_query,
        max_results=10000  # Adjust based on expected volume
    )

    print("\n" + "=" * 70)
    xrl_counts = count_papers_by_year(
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

    # Create visualization
    print("\n" + "=" * 70)
    print("CREATING VISUALIZATION")
    print("=" * 70)

    create_comparison_chart(xai_counts, xrl_counts)

    # Save data
    save_results_to_csv(xai_counts, xrl_counts)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
