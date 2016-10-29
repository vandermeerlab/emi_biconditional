import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("white")
sns.set_style("ticks")


def plot_behavior(df, rats, filepath=None, only_sound=False, by_outcome=False):
    rat_idx = np.zeros(len(df), dtype=bool)
    for rat in rats:
        rat_idx = rat_idx | (df['rat'] == rat)
    rats_df = df[rat_idx]

    if only_sound:
        colours = ["#4393c3", "#b2182b", "#d6604d", "#2166ac"]
    else:
        colours = ["#9970ab", "#4393c3", "#762a83", "#b2182b", "#5aae61", "#d6604d", "#1b7837", "#2166ac"]

    g = sns.FacetGrid(data=rats_df, col="measure", sharey=False, size=3, aspect=1.)
    if by_outcome:
        colours = ["#9970ab", "#d6604d", "#1b7837", "#2166ac"]
        g.map_dataframe(sns.tsplot, time="session", unit="trial", condition="rewarded", value="value", color=colours)
        legend_dist = 1.8
    else:
        g.map_dataframe(sns.tsplot, time="session", unit="trial", condition="condition", value="value", color=colours)
        legend_dist = 1.5
    g.set_axis_labels("Session", "Value")
    for ax, label in zip(g.axes[0], ["Duration in food cup (s)",
                                     "# of entries",
                                     "Latency to first entry (s)",
                                     "Percent responses"]):
        ax.set_title("")
        ax.set_ylabel(label)
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(legend_dist, 1.))
    if filepath is not None:
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
