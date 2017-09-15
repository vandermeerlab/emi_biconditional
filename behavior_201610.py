import measurements as m
from core import Experiment, Rat, TrialEpoch


expt = Experiment(
    name="201704",
    cache_key="epoch",
    trial_epochs=[
        TrialEpoch("mags", start_idx=1, stop_idx=2),
        TrialEpoch("baseline", start_idx=4, duration=-10),
        TrialEpoch("baseline", start_idx=6, duration=-10),
        TrialEpoch("light1", start_idx=4, stop_idx=5),
        TrialEpoch("light2", start_idx=6, stop_idx=7),
        TrialEpoch("sound1", start_idx=8, stop_idx=9),
        TrialEpoch("sound2", start_idx=10, stop_idx=11),
        TrialEpoch("trial1", start_idx=12, stop_idx=13),
        TrialEpoch("trial2", start_idx=14, stop_idx=15),
        TrialEpoch("trial3", start_idx=16, stop_idx=17),
        TrialEpoch("trial4", start_idx=18, stop_idx=19),
    ],
    measurements=[m.Duration(), m.Count(), m.Latency(), m.AtLeastOne()],
    rats=[
        Rat('1', group="1"),
        Rat('2', group="2"),
        Rat('3', group="1"),
        Rat('4', group="2"),
        Rat('5', group="1"),
        Rat('6', group="2"),
        Rat('7', group="1"),
        Rat('8', group="2"),
    ],
    magazine_session='!2016-10-18',
)


def add_datapoints(session, data, rat):

    def add_data(cue, trial=None):
        if trial is not None:
            meta = {
                "cue_type": cue[:-1],
                "trial_type": trial[-1],
                "rewarded": "rewarded" if trial[-1] in ("2", "4") else "unrewarded",
                "cue": cue,
            }
            trial = data[trial]
            cue = data[cue]
            session.add_epoch_data(rat.rat_id, trial.intersect(cue), meta)
        else:
            meta = {
                "cue_type": cue,
                "trial_type": "",
                "rewarded": "",
                "cue": cue,
            }
            session.add_epoch_data(rat.rat_id, data[cue], meta)

    if rat.group == "1":
        add_data("light1", "trial1")
        add_data("sound2", "trial1")
        add_data("light1", "trial2")
        add_data("sound1", "trial2")
        add_data("light2", "trial3")
        add_data("sound1", "trial3")
        add_data("light2", "trial4")
        add_data("sound2", "trial4")
        add_data("baseline")

    elif rat.group == "2":
        add_data("light2", "trial1")
        add_data("sound2", "trial1")
        add_data("light2", "trial2")
        add_data("sound1", "trial2")
        add_data("light1", "trial3")
        add_data("sound1", "trial3")
        add_data("light1", "trial4")
        add_data("sound2", "trial4")
        add_data("baseline")


expt.add_datapoints = add_datapoints
expt.plot_all(change=[35, 46, 52])





import os

import nept
from core import combine_rats, Rat
from load_data import assign_medpc_label
from plotting import plot_behavior, plot_duration


thisdir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(thisdir, 'cache', 'data', 'med_fall2016')
output_filepath = os.path.join(thisdir, 'plots', 'fall2016')

broken_sessions = ['!2016-10-19a1', '!2016-10-19a2']
extended = ['!2016-11-28', '!2016-11-29', '!2016-11-30', '!2016-12-01', '!2016-12-02', '!2016-12-03',
            '!2016-12-06', '!2016-12-07a', '!2016-12-07b', '!2016-12-08', '!2016-12-09']
sessions = []
extended_sessions = []
for file in sorted(os.listdir(data_filepath)):
    if file[0] == '!' and file not in broken_sessions and file not in extended:
        sessions.append(os.path.join(data_filepath, file))
    if file[0] == '!' and file not in broken_sessions and file in extended:
        extended_sessions.append(os.path.join(data_filepath, file))

rats = ['1', '2', '3', '4', '5', '6', '7', '8']
group1 = ['1', '3', '5', '7']
group2 = ['2', '4', '6', '8']

plot_extended = False
if plot_extended:
    rats = ['5', '8']
    sessions = extended_sessions

data = dict()
for rat in rats:
    data[rat] = Rat(rat, group1, group2)

broken_a = os.path.join(data_filepath, broken_sessions[0])
broken_b = os.path.join(data_filepath, broken_sessions[1])
rats_data_a = nept.load_medpc(broken_a, assign_medpc_label)
rats_data_b = nept.load_medpc(broken_b, assign_medpc_label)

for rat in rats_data_a:
    for key in rats_data_a[rat]:
        rats_data_b[rat][key].join(rats_data_a[rat][key])
for rat in rats:
    data[rat].add_session_medpc(**rats_data_b[rat])

for session in sessions:
    rats_data = nept.load_medpc(os.path.join(data_filepath, session), assign_medpc_label)

    for rat in rats:
        data[rat].add_session_medpc(**rats_data[rat])

n_sessions = len(data[rats[0]].sessions)
only_sound = False

df = combine_rats(data, rats, n_sessions, only_sound)

if 1:
    for by_outcome in [True, False]:
        for rat in rats:
            if only_sound:
                filename = 'sound_rat' + rat + '_behavior.png'
            elif by_outcome:
                filename = 'outcome_rat' + rat + '_behavior.png'
            else:
                filename = 'trials_rat' + rat + '_behavior.png'
            filepath = os.path.join(output_filepath, filename)
            plot_behavior(df, [rat], filepath, only_sound=only_sound, by_outcome=by_outcome,
                          change_sessions=[35, 46, 52])

        filenames = ['trials_group1_behavior.png', 'trials_group2_behavior.png',
                     'trials_all-rats_behavior.png', 'trials_exp-rats_behavior.png',
                     'trials_bucci-rats_behavior.png']
        sound_filenames = ['sound_group1_behavior.png', 'sound_group2_behavior.png',
                           'sound_all-rats_behavior.png', 'sound_exp-rats_behavior.png',
                           'sound_bucci-rats_behavior.png']
        outcome_filenames = ['outcome_group1_behavior.png', 'outcome_group2_behavior.png',
                             'outcome_all-rats_behavior.png', 'outcome_exp-rats_behavior.png',
                             'outcome_bucci-rats_behavior.png']
        rat_groups = [['1', '3', '5', '7'], ['2', '4', '6', '8'], rats, ['1', '2', '3', '5', '6', '7', '8'],
                      ['1', '2', '3', '4', '5', '6']]

        for i, rat in enumerate(rat_groups):
            if only_sound:
                filepath = os.path.join(output_filepath, sound_filenames[i])
            elif by_outcome:
                filepath = os.path.join(output_filepath, outcome_filenames[i])
            else:
                filepath = os.path.join(output_filepath, filenames[i])
            plot_behavior(df, rat, filepath, only_sound=only_sound, by_outcome=by_outcome, change_sessions=[35, 46, 52])

if 1:
    for rat in rats:
        filename = rat + '_outcome_duration.png'
        filepath = os.path.join(output_filepath, filename)
        plot_duration(df, [rat], filepath, by_outcome=True, ymax=10.)

if 1:
    by_outcome = True
    filenames = ['group1_medpc.png', 'group2_medpc.png', 'all-rats_medpc.png']
    rat_groups = [group1, group2, rats]

    for i, rat in enumerate(rat_groups):
        filepath = os.path.join(output_filepath, filenames[i])
        plot_duration(df, rat, filepath, by_outcome=by_outcome, ymax=10.)


    # def add_session_medpc(self, mags, pellets, lights1, lights2, sounds1, sounds2,
    #                       n_unique=8, delay=5.02, tolerance=1e-08):
    #     """Sorts cues into appropriate trials (1, 2, 3, 4), using specified delay between light and sound cues."""

    #     session = Session(mags, pellets)

    #     for trial in [1, 2, 3, 4]:
    #         if self.light_trials[trial] == 'lights1':
    #             light_cues = lights1
    #         elif self.light_trials[trial] == 'lights2':
    #             light_cues = lights2
    #         if self.sound_trials[trial] == 'sounds1':
    #             sound_cues = sounds1
    #         elif self.sound_trials[trial] == 'sounds2':
    #             sound_cues = sounds2

    #         n_trials = 0
    #         for light in light_cues:
    #             for sound in sound_cues:
    #                 if np.allclose(sound.start - light.stop, delay, atol=tolerance):
    #                     session.add_trial(light, 'light', trial)
    #                     session.add_trial(sound, 'sound', trial)
    #                     n_trials += 1

    #         for _ in range(n_unique - n_trials):
    #             session.add_missing_trial('light', trial)
    #             session.add_missing_trial('sound', trial)

    #     self.sessions.append(session)