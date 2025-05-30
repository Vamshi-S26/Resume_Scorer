import matplotlib.pyplot as plt
import numpy as np

# Color-blind friendly palette
COLOR_MATCHED = '#1b9e77'  # Teal
COLOR_MISSING = '#d95f02'  # Orange
COLOR_SELECTED = '#2ca02c'  # Green
COLOR_REJECTED = '#d62728'  # Red

def plot_grouped_bar_chart(results, show=True, save_path=None):
    if not results:
        print("No data to visualize.")
        return

    roles = [res['role'] for res in results]
    matched_counts = [len(res['matched_skills']) for res in results]
    missing_counts = [len(res['missing_skills']) for res in results]

    x = np.arange(len(roles))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar(x - width / 2, matched_counts, width, label='Matched Skills', color=COLOR_MATCHED)
    bars2 = ax.bar(x + width / 2, missing_counts, width, label='Missing Skills', color=COLOR_MISSING)

    ax.set_xlabel('Roles')
    ax.set_ylabel('Number of Skills')
    ax.set_title('Matched vs Missing Skills per Role')
    ax.set_xticks(x)
    ax.set_xticklabels(roles, rotation=45, ha='right')
    ax.legend()

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
    if show:
        plt.show()
    else:
        return fig


def plot_lollipop_chart(results, show=True, save_path=None):
    if not results:
        print("No data to visualize.")
        return

    roles = [res['role'] for res in results]
    scores = [float(res['match_score']) for res in results]
    predictions = [res['prediction'] for res in results]

    x = np.arange(len(roles))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.vlines(x, 0, scores, color='skyblue', linewidth=3)

    colors = [COLOR_SELECTED if p == 'Selected' else COLOR_REJECTED for p in predictions]
    ax.scatter(x, scores, color=colors, s=100)

    ax.set_xticks(x)
    ax.set_xticklabels(roles, rotation=45, ha='right')
    ax.set_ylim(0, 110)
    ax.set_ylabel('Match Score (%)')
    ax.set_title('Match Scores by Role (Green = Selected, Red = Rejected)')

    for i, score in enumerate(scores):
        ax.text(i, score + 2, f"{score:.1f}%", ha='center', va='bottom')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
    if show:
        plt.show()
    else:
        return fig
