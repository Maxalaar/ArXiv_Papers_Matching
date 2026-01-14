from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional


def plot_papers_per_year(df: pd.DataFrame,
                         title: str = "Number of Papers Published per Year",
                         figsize: tuple = (12, 6),
                         color: str = 'steelblue',
                         path: Optional[Path] = None) -> None:
    """
    Create a bar chart showing the number of papers published per year.

    Args:
        df: DataFrame from arxiv_query_to_dataframe function
        title: Title for the plot
        figsize: Figure size (width, height)
        color: Color for the bars
        path: Optional path to save the figure (e.g., 'papers_per_year.png')

    Returns:
        None (displays the plot)
    """
    if df.empty:
        print("DataFrame is empty. No data to plot.")
        return

    # Check if 'year' column exists
    if 'year' not in df.columns:
        print("Error: DataFrame must contain a 'year' column.")
        return

    # Count papers per year
    papers_per_year = df['year'].value_counts().sort_index()

    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)

    # Create bar chart
    bars = ax.bar(papers_per_year.index.astype(str), papers_per_year.values, color=color)

    # Customize the plot
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Number of Papers', fontsize=12)

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontsize=10)

    # Rotate x-axis labels for better readability if many years
    if len(papers_per_year) > 5:
        plt.xticks(rotation=45, ha='right')

    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Save figure if path is provided
    if path:
        plt.savefig(path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to: {path}")
