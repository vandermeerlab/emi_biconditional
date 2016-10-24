import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from core import f_analyze

sns.set_style("white")
sns.set_style("ticks")


def plot_behavior(data, rats, n_sessions, filepath=None, only_sound=False):
    measures = ['durations', 'numbers', 'latency', 'responses']
    together = dict(trial=[], rat=[], session=[], trial_type=[], cue=[], value=[], measure=[], condition=[])

    for session in range(n_sessions):
        all_trials = []
        for rat in rats:
            all_trials.extend(data[rat].sessions[session].trials)

            for i, trial in enumerate(all_trials):
                for measure in measures:
                    if not only_sound or trial.cue == 'sound':
                        together['trial'].append("%s, %d" % (rat, i))
                        together['rat'].append(rat)
                        together['session'].append(session+2)
                        together['trial_type'].append(trial.trial_type)
                        together['cue'].append(trial.cue)
                        together['condition'].append("%s %d" % (trial.cue, trial.trial_type))
                        together['measure'].append(measure)
                        together['value'].append(f_analyze(trial, measure))

    df = pd.DataFrame(data=together)

    if only_sound:
        colours = ["#4393c3", "#b2182b", "#d6604d", "#2166ac"]
    else:
        colours = ["#9970ab", "#4393c3", "#762a83", "#b2182b", "#5aae61", "#d6604d", "#1b7837", "#2166ac"]

    g = sns.FacetGrid(data=df, col="measure", sharey=False, size=3, aspect=1.)
    g.map_dataframe(sns.tsplot, time="session", unit="trial", condition="condition", value="value", color=colours)
    g.set_axis_labels("Session", "Value")
    for ax, label in zip(g.axes[0], ["Durations", "Numbers", "Latency", "Responses"]):
        ax.set_title("")
        ax.set_ylabel(label)
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(1.5, 1.))
    if filepath is not None:
        plt.savefig(filepath, bbox_inches='tight')
    else:
        plt.show()
