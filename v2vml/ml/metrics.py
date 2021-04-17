from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report


class FinalizedError(Exception):

    def __init__(self, message='Cannot add to finalized CustomMetrics'):
        self.message = message
        super().__init__(self.message)


class CustomMetrics(ABC):

    def __init__(self, index=None):

        self.total_adds = 0
        self.final_total = 0
        self.is_finalized = False
        self.is_init = False

        self.index = None
        if index:
            self.index = index

        super().__init__()

    @abstractmethod
    def _create(self, actual_values, predictions):
        pass

    @abstractmethod
    def _init_add(self, actual_values, predictions):
        pass

    @abstractmethod
    def _add(self, actual_values, predictions):
        pass

    def add(self, actual_values, predictions) -> None:

        if self.is_finalized:
            raise FinalizedError

        if self.is_init:
            self._add(actual_values, predictions)

        else:
            self.is_init = True
            self._init_add(actual_values, predictions)

        self.total_adds += 1

    def finalize(self):
        self._finalize()
        self.final_total = self.total_adds
        self.total_adds = 0
        self.is_finalized = True

    @abstractmethod
    def _finalize(self):
        pass

    @abstractmethod
    def get_copy(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Accuracy(CustomMetrics):

    # index parameter is unused, but kept for consistency
    def __init__(self, index=None):

        self.accuracy = 0
        super().__init__(index=index)

    def _create(self):
        pass

    def _init_add(self, actual_values, predictions):
        self._add(actual_values, predictions)

    def _add(self, actual_values, predictions):
        self.accuracy += accuracy_score(actual_values, predictions)

    def _finalize(self):
        self.accuracy = self.accuracy / self.total_adds

    def get_copy(self):
        return self.accuracy

    def __str__(self):
        return str(self.accuracy)


class Report(CustomMetrics):

    def __init__(self, index=None):

        self.report = None
        self.rows = None
        self.cols = None
        super().__init__(index=index)

    def _create(self, actual_values, predictions):
        return classification_report(actual_values, predictions, output_dict=True)

    def _init_add(self, actual_values, predictions):
        self.report = self._create(actual_values, predictions)
        self.rows = list(self.report.keys())
        self.cols = list(self.report[self.rows[0]].keys())

    def _add(self, actual_values, predictions):

        report = self._create(actual_values, predictions)
        rows = list(self.report.keys())
        for r in rows:

            # average is a single value, not a dictionary
            if 'accuracy' == r:
                self.report[r] += report[r]
                continue

            cols = list(self.report[r].keys())
            for c in cols:
                self.report[r][c] += report[r][c]

    def __as_dataframe(self) -> pd.DataFrame:

        # all classification reports have 4 columns
        cr_frame = pd.DataFrame(np.zeros((len(list(self.report.keys())), 4)))
        cr_frame.index = self.rows
        cr_frame.columns = self.cols

        for i in np.arange(len(self.rows)):

            r = self.rows[i]

            # average is a single value, not a dictionary
            if 'accuracy' == r:
                # average -> precision
                cr_frame.iloc[-3, -4] = np.nan
                # average -> recall
                cr_frame.iloc[-3, -3] = np.nan
                # average -> f1-score
                cr_frame.iloc[-3, -2] = self.report[r]
                # average -> support
                cr_frame.iloc[-3, -1] = self.report['macro avg']['support']
                continue

            for j in np.arange(len(self.cols)):
                c = self.cols[j]
                cr_frame.iloc[i, j] = self.report[r][c]

        # update row labels
        if self.index:
            updated_index = list(self.index).copy()
            updated_index.extend(cr_frame.index[-3::])
            cr_frame.index = updated_index

        return cr_frame

    def _finalize(self):

        cr_frame = self.__as_dataframe()

        # remember that self.report is still a dictionary at this point
        for i in np.arange(len(self.rows)):

            r = self.rows[i]

            # average is a single value, not a dictionary
            if 'accuracy' == r:
                # average -> f1-score
                cr_frame.iloc[-3, -2] = round(self.report[r] / self.total_adds, 2)
                # average -> support
                cr_frame.iloc[-3, -1] = round(self.report['macro avg']['support'] / self.total_adds, 2)
                continue

            for j in np.arange(len(self.cols)):
                c = self.cols[j]
                cr_frame.iloc[i, j] = round(self.report[r][c] / self.total_adds, 2)

        # self.report is now a dataframe
        self.report = cr_frame

    def get_copy(self):

        # if report has not been finalized and is a dictionary
        if type(self.report) == dict:
            return self.__as_dataframe().copy()

        # if report has been finalized and is a dataframe
        else:
            return self.report.copy()

    def __str__(self):
        return str(self.report)


class Stats(CustomMetrics):

    def __init__(self, index=None):

        self.stats = None
        super().__init__(index=index)

    def _create(self, actual_values, predictions) -> pd.DataFrame:

        num_rows = len(list(set(actual_values)))
        num_cols = (num_rows * 2) + 1
        stats = pd.DataFrame(np.zeros((num_rows, num_cols)))

        # custom row labels
        if self.index:
            stats.index = self.index
        # default row labels
        else:
            stats.index = set(actual_values)

        columns = []

        # Labelled as...
        for i in stats.index:
            columns.append('Labelled ' + str(i))

        # Percent labelled as...
        for i in stats.index:
            columns.append('Percent ' + str(i))

        columns.append('Total')
        stats.columns = columns

        for y_test, y_pred in zip(actual_values, predictions):
            # indexing must be done with ints, not floats
            y_test = int(y_test)
            y_pred = int(y_pred)

            # total of node type
            stats.iloc[y_test, -1] += 1

            # labelled as
            stats.iloc[y_test, y_pred] += 1

        return stats

    def _init_add(self, actual_values, predictions):
        self.stats = self._create(actual_values, predictions)

    def _add(self, actual_values, predictions) -> None:

        stats = self._create(actual_values, predictions)
        num_rows = len(stats.index)
        # update values for 'Labelled...'
        for i in np.arange(num_rows):
            for j in np.arange(num_rows):
                self.stats.iloc[i, j] += stats.iloc[i, j]

        # update values for the totals column
        for i in np.arange(num_rows):
            self.stats.iloc[i, -1] += stats.iloc[i, -1]

    def _finalize(self):

        num_rows = len(self.stats.index)
        for i in np.arange(num_rows):
            for j in np.arange(num_rows):
                self.stats.iloc[i, j + num_rows] = round(100 * (self.stats.iloc[i, j] / self.stats.iloc[i, -1]), 2)

    def get_copy(self) -> pd.DataFrame:
        return self.stats.copy()

    def __str__(self):
        return str(self.stats)


class StatSuite(CustomMetrics):

    def __init__(self, index=None):

        self.metrics = []

        self.accuracy = Accuracy(index=index)
        self.report = Report(index=index)
        self.stats = Stats(index=index)

        self.metrics.append(self.accuracy)
        self.metrics.append(self.report)
        self.metrics.append(self.stats)

        super().__init__(index=index)

    def _create(self, actual_values, predictions):
        pass

    def _init_add(self, actual_values, predictions):
        self._add(actual_values, predictions)

    def _add(self, actual_values, predictions):
        for m in self.metrics:
            m.add(actual_values, predictions)

    def _finalize(self):
        for m in self.metrics:
            m.finalize()

    def get_copy(self):
        return [m.get_copy() for m in self.metrics]

    def __str__(self):

        s = 'Iterations:' + str(self.final_total) + '\n\n'
        s += 'Accuracy:' + str(self.accuracy) + '\n\n'
        s += 'Classification Report:\n\n' + str(self.report) + '\n\n'
        s += 'Prediction Details:\n\n' + str(self.stats)
        return s
