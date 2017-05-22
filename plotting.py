import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

sns.set_style("white")
sns.set_style("ticks")


def plot_behavior(df, rats, filepath=None, only_sound=False, by_outcome=False, change_sessions=None, xlim=None):
    if change_sessions is None:
        change_sessions = []

    rat_idx = np.zeros(len(df), dtype=bool)
    for rat in rats:
        rat_idx = rat_idx | (df['rat'] == rat)
    rats_df = df[rat_idx]

    if only_sound:
        colours = ["#4393c3", "#b2182b", "#d6604d", "#2166ac", 'k', '#fe9929', '#f768a1']
    else:
        colours = ["#9970ab", "#4393c3", "#762a83", "#b2182b", "#5aae61",
                   "#d6604d", "#1b7837", "#2166ac", 'k', '#fe9929', '#f768a1']

    g = sns.FacetGrid(data=rats_df, col="measure", sharey=False, size=3, aspect=1.)
    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)))
    if by_outcome:
        colours = ["#9970ab", "#d6604d", "#1b7837", "#2166ac", 'k', '#fe9929', '#f768a1']
        g.map_dataframe(sns.tsplot, time="session", unit="trial", condition="rewarded", value="value",
                        err_style="ci_band", ci=68, color=colours)
        legend_dist = 1.
    else:
        g.map_dataframe(sns.tsplot, time="session", unit="trial", condition="condition", value="value",
                        err_style="ci_band", ci=68, color=colours)
        legend_dist = 1.
    g.set_axis_labels("Session", "Value")
    for ax, label in zip(g.axes[0], ["Duration in food cup (s)",
                                     "# of entries",
                                     "Latency to first entry (s)",
                                     "Percent responses"]):
        ax.set_title("")
        ax.set_ylabel(label)

        if len(change_sessions) == 1:
            ax.axvspan(change_sessions[0], rats_df['session'].max(), color='#cccccc', alpha=0.3)
        elif len(change_sessions) == 2:
            ax.axvspan(change_sessions[0], change_sessions[1]-1, color='#cccccc', alpha=0.3)
        elif len(change_sessions) == 3:
            ax.axvspan(change_sessions[0], change_sessions[1]-1, color='#cccccc', alpha=0.3)
            ax.axvspan(change_sessions[2], rats_df['session'].max(), color='#cccccc', alpha=0.3)

        if xlim is not None:
            ax.set_xlim(xlim)

    plt.tight_layout()
    plt.legend(bbox_to_anchor=(legend_dist, 1.))
    if filepath is not None:
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_duration(df, rats, filepath=None, only_sound=False, by_outcome=False, change_sessions=None,
                  xlim=None, ymax=None):

    if change_sessions is None:
        change_sessions = []

    rat_idx = np.zeros(len(df), dtype=bool)
    for rat in rats:
        rat_idx = rat_idx | (df['rat'] == rat)
    rats_df = df[rat_idx]

    if only_sound:
        colours = ["#4393c3", "#b2182b", "#d6604d", "#2166ac", 'k', '#fe9929', '#f768a1']
    else:
        colours = ["#9970ab", "#4393c3", "#762a83", "#b2182b", "#5aae61",
                   "#d6604d", "#1b7837", "#2166ac", 'k', '#fe9929', '#f768a1']

    duration = rats_df.loc[rats_df.measure == 'durations']

    f, ax = plt.subplots(figsize=(5, 4))

    if by_outcome:
        colours = ["#9970ab", "#d6604d", "#1b7837", "#2166ac", 'k', '#fe9929', '#f768a1']
        ax = sns.tsplot(data=duration, time="session", unit="trial", condition="rewarded", value="value",
                        err_style="ci_band", ci=68, color=colours)
        legend_dist = 1.
    else:
        ax = sns.tsplot(data=duration, time="session", unit="trial", condition="condition", value="value",
                        err_style="ci_band", ci=68, color=colours)
        legend_dist = 1.

    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)))
    ax.set(xlabel='Session', ylabel='Duration in food cup (s)')

    if len(change_sessions) == 1:
        ax.axvspan(change_sessions[0], rats_df['session'].max(), color='#cccccc', alpha=0.3)
    elif len(change_sessions) == 2:
        ax.axvspan(change_sessions[0], change_sessions[1]-1, color='#cccccc', alpha=0.3)
    elif len(change_sessions) == 3:
        ax.axvspan(change_sessions[0], change_sessions[1]-1, color='#cccccc', alpha=0.3)
        ax.axvspan(change_sessions[2], rats_df['session'].max(), color='#cccccc', alpha=0.3)

    if xlim is not None:
        ax.set_xlim(xlim)

    if ymax is not None:
        ax.set_ylim(0, ymax)

    sns.despine()
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(legend_dist, 1.))
    if filepath is not None:
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
