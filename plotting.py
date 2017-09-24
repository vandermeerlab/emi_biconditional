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


def plot_behavior(df, rats, filepath=None, colours=None, only_sound=False, by_outcome=False,
                  change_sessions=None, xlim=None, measure=None):
    if change_sessions is None:
        change_sessions = []
    if colours is None:
        raise ValueError("must specify a list of colours")

    rat_idx = np.zeros(len(df), dtype=bool)
    for rat in rats:
        rat_idx = rat_idx | (df['rat'] == rat.rat_id)
    rats_df = df[rat_idx]

    if measure is not None:
        rats_df = rats_df.loc[rats_df.measure == measure]

    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)))
    if by_outcome:
        rats_df = add_col(rats_df, "unit", "cue", "rat", "trial")
        rats_df = add_col(rats_df, "condition", "cue_type", "rewarded")
    else:
        rats_df = add_col(rats_df, "unit", "rat", "trial")
        rats_df = add_col(rats_df, "condition", "cue", "rewarded")
    g = sns.FacetGrid(data=rats_df, col="measure", sharey=False, size=3, aspect=1.)
    g.map_dataframe(sns.tsplot, time="session", unit="unit", condition="condition", value="value",
                    err_style="ci_band", ci=68, color=colours)
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
    handles, labels = ax.get_legend_handles_labels()
    sortedhl = sorted(zip(handles, labels), key=lambda x: x[1])
    plt.legend(*zip(*sortedhl), bbox_to_anchor=(1., 1.))
    if filepath is not None:
        mkdirs(os.path.dirname(filepath))
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def plot_overtime(df, rats, filepath=None):
    rat_idx = np.zeros(len(df), dtype=bool)
    for rat in rats:
        rat_idx = rat_idx | (df['rat'] == rat.rat_id)
    rats_df = df[rat_idx]

    df = add_col(df, "unit", "rat", "trial", "session")
    g = sns.FacetGrid(data=df, col="duration", sharey=False, size=3, aspect=1.)
    g.map_dataframe(sns.tsplot, time="time_start", unit="unit", condition="cue", value="value",
                    err_style="ci_band", ci=68, color="deep")

    ylim = 0
    for ax in g.axes[0]:
        ax.set_ylabel("Duration in food cup (s)")
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
