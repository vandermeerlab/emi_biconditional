import errno
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns

sns.set_style("white")
sns.set_style("ticks")


def mkdirs(dirs):
    try:
        os.makedirs(dirs)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def add_col(df, name, *columns):
    fmt = ", ".join(["{}" for _ in range(len(columns))])

    def to_apply(row):
        return fmt.format(*(row[col] for col in columns))
    return df.assign(**{name: df.apply(to_apply, axis="columns")})


def plot_behavior(df, rats, filepath=None, labels=None, colours=None, by_outcome=False,
                  change_sessions=None, xlim=None, measure=None, diff_targets=True):
    if change_sessions is None:
        change_sessions = []

    n_sessions = max(df['session'])

    if labels is None:
        labels = ["Duration in food cup (s)",
                  "Number of entries",
                  "Latency to first entry (s)",
                  "Percent responses"]
    if colours is None:
        colours = 'Paired'

    rat_idx = np.zeros(len(df), dtype=bool)
    for rat in rats:
        rat_idx = rat_idx | (df['rat'] == rat.rat_id)
    rats_df = df[rat_idx]

    if measure is not None:
        rats_df = rats_df.loc[rats_df.measure == measure]

    if by_outcome and diff_targets:
        rats_df = add_col(rats_df, "unit", "cue_type", "rat", "trial")
        rats_df = add_col(rats_df, "condition", "cue", "rewarded")
    elif by_outcome and not diff_targets:
        rats_df = add_col(rats_df, "unit", "cue_type", "rat", "trial")
        rats_df = add_col(rats_df, "condition", "cue_type", "rewarded")
    else:
        rats_df = add_col(rats_df, "unit", "rat", "trial")
        rats_df = add_col(rats_df, "condition", "cue", "rewarded")
    g = sns.FacetGrid(data=rats_df, col="measure", sharey=False, size=3, aspect=1.)
    g.map_dataframe(sns.tsplot, time="session", unit="unit", condition="condition", value="value",
                    err_style="ci_band", ci=68, color=colours)
    g.set_axis_labels("Session", "Value")

    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)))

    for ax, label in zip(g.axes[0], labels):
        ax.set_title("")
        ax.set_ylabel(label)

        for start, stop in zip(change_sessions[::2], change_sessions[1::2]):
            ax.axvspan(start, stop, alpha=0.3, color='#bdbdbd')
        if len(change_sessions) % 2 == 1:
            ax.axvspan(change_sessions[-1], n_sessions, alpha=0.3, color='#bdbdbd')

        if xlim is not None:
            ax.set_xlim(xlim)

    handles, labels = plt.gca().get_legend_handles_labels()
    sortedhl = sorted(zip(handles, labels), key=lambda x: x[1])
    plt.gca().legend(*zip(*sortedhl), bbox_to_anchor=(1., 1.))

    plt.tight_layout()

    if filepath is not None:
        mkdirs(os.path.dirname(filepath))
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_overtime(df, rats, measure=None, labels=None, colours=None, filepath=None):
    if measure is None:
        raise ValueError("must include a measure. Duration, Count, Latency, "
                         "or AtLeastOne are all acceptable measures.")

    if colours is None:
        colours = "deep"

    rat_idx = np.zeros(len(df), dtype=bool)
    for rat in rats:
        rat_idx = rat_idx | (df['rat'] == rat.rat_id)
    rats_df = df[rat_idx]

    if measure is not None:
        rats_df = rats_df.loc[rats_df.measure == measure]

    rats_df = add_col(rats_df, "unit", "rat", "trial", "session")
    g = sns.FacetGrid(data=rats_df, col="duration", sharey=False, size=3, aspect=1.)
    g.map_dataframe(sns.tsplot, time="time_start", unit="unit", condition="cue", value="value",
                    err_style="ci_band", ci=68, color=colours)

    ylim = 0
    for ax in g.axes[0]:
        ax.set_ylabel(labels)
        if ax.get_ylim()[1] > ylim:
            ylim = ax.get_ylim()[1]

    for ax in g.axes[0]:
        ax.set_ylim(0, ylim)

    plt.tight_layout()
    handles, labels = ax.get_legend_handles_labels()
    sortedhl = sorted(zip(handles, labels), key=lambda x: x[1])
    plt.legend(*zip(*sortedhl), bbox_to_anchor=(1., 1.))

    plt.tight_layout()
    if filepath is not None:
        mkdirs(os.path.dirname(filepath))
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
