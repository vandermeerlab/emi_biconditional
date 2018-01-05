import numpy as np


def check_sequence(sequence, n_row):
    """Checks the sequence

    Parameters
    ----------
    sequence : list of ints
    n_row : int

    Returns
    -------
    boolean

    """
    if n_row <= 1:
        raise ValueError("n_row must be >= 2")
    trials = np.unique(sequence)

    for trial in trials:
        start, end = None, None
        for i, x in enumerate(sequence):
            if x == trial and start is None:
                start = i
            if x != trial and start is not None and end is None:
                end = i-1
            if start is not None and end is not None:
                if end-start+1 > n_row:
                    return False
                else:
                    start, end = None, None

    return True


def check_trial_prior(sequence, trial, n_prior):
    """Checks the correct number of prior trials of the same type

    Parameters
    ----------
    sequence : list of ints
    trial : int
    n_prior : int

    Returns
    -------
    boolean

    """
    trials = np.unique(sequence)
    counts = {trial: 0 for trial in trials}

    for i, x in enumerate(sequence):
        if x == trial:
            counts[sequence[i-1]] += 1

    return not any(trial_val > n_prior for trial_val in counts.values())


def check_prior(sequence, n_prior):
    """Checks the prior trials

    Parameters
    ----------
    sequence : list of ints
    n_prior : int

    Returns
    -------
    boolean

    """
    trials = np.unique(sequence)
    return all(check_trial_prior(sequence, trial, n_prior) for trial in trials)


def find_sequence(trial_types, n_row, n_prior, n_sequences):
    """Finds sequences that have fewer than x of the same
       trial type or reward outcome in a row.

       Parameters
       ----------
       trial_types : list of ints
       n_row : int
           Number of same trial types allowed in a row.
       n_prior : int
           Number of trial type
       n_sequences : int
           Number of trials in a sequence

       Returns
       -------
       sequences : list of lists

    """
    sequences = []

    while len(sequences) < n_sequences:
        np.random.shuffle(trial_types)
        sequence = trial_types.copy()
        outcome_sequence = [x % 2 for x in sequence]

        if not check_sequence(sequence, n_row):
            continue
        if not check_sequence(outcome_sequence, n_row):
            continue
        if not check_prior(sequence, n_prior):
            continue

        sequences.append(sequence)

    return sequences


def find_iti(iti_lengths, n_row, n_sequences):
    """Finds sequences that have fewer than x of the same iti type in a row.

       Parameters
       ----------
       iti_lengths : list of strs
       n_row : int
           Number of same trial types allowed in a row.
       n_sequences : int
           Number of trials in a sequence

       Returns
       -------
       sequences : list of lists

    """
    sequences = []

    while len(sequences) < n_sequences:
        np.random.shuffle(iti_lengths)
        sequence = iti_lengths.copy()

        if not check_sequence(sequence, n_row):
            continue
        sequences.append('[%s]' % '", '.join(map(str, sequence)))

    return sequences


# feature_lengths = [150, 180, 210, 240, 270,
#                    150, 180, 210, 240, 270,
#                    150, 180, 210, 240, 270,
#                    150, 180, 210, 240, 270,
#                    150, 180, 210, 240, 270,
#                    150, 180, 210, 240, 270]
# trial_types = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#                2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

# feature_lengths = [150, 180, 210, 240, 270,
#                    150, 180, 210, 240, 270,
#                    150, 180, 210, 240, 270,
#                    150, 180, 210, 240, 270,
#                    150, 180, 210, 240, 270,
#                    180, 210, 240]
# trial_types = [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2,
#                3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4]

feature_lengths = [150, 180, 210, 240, 270,
                   150, 180, 210, 240, 270,
                   150, 180, 210, 240, 270,
                   150, 180, 210, 240, 270,
                   150, 180, 210, 240, 270,
                   180, 210, 240]
# trial_types = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
#                4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

# trial_types = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#                2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

trial_types = [3, 3, 3, 3, 3, 3, 3,
               4, 4, 4, 4, 4, 4, 4]

# trial_types = [1, 1, 1, 1, 1, 1, 1,
#                2, 2, 2, 2, 2, 2, 2]

sequences = find_sequence(trial_types, n_row=4, n_prior=10, n_sequences=20)
print('Sequence length is:', len(sequences[0]))

print(sequences)


feature_sequences = find_iti(feature_lengths, n_row=3, n_sequences=20)

print(feature_sequences)
