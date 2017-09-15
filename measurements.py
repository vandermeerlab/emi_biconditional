import numpy as np


class Measurement:
    def __init__(self, label=None):
        if label is None:
            label = type(self).__name__
        self.label = label

    def measure(self, trial, epoch_of_interest):
        raise NotImplementedError("Subclasses must implement")

    def __call__(self, epoch, epoch_of_interest):
        measures = []
        for i, trial in enumerate(epoch):
            measures.append(self.measure(trial, epoch_of_interest))
        return np.array(measures, dtype=float)


class AtLeastOne(Measurement):
    def measure(self, trial, epoch_of_interest):
        return trial.intersect(epoch_of_interest).n_epochs > 0


class Count(Measurement):
    def measure(self, trial, epoch_of_interest):
        return trial.intersect(epoch_of_interest).n_epochs


class Duration(Measurement):
    def measure(self, trial, epoch_of_interest):
        return np.sum(trial.intersect(epoch_of_interest).durations)


class Latency(Measurement):
    def measure(self, trial, epoch_of_interest):
        occurrences = trial.intersect(epoch_of_interest)
        if occurrences.n_epochs > 0:
            return occurrences.start - trial.start
        else:
            return trial.durations[0]
