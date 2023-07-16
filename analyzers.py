import numpy as np


class Analyzer:
    """
    This class acts as an analyzer for the given data set
    It provides the mean, median, mode, min value, max value and
    correlations for the given dataset.
    """

    def __init__(self, importer, num_correlations=5) -> None:
        self._data = importer.data
        self._headers = self._get_headers()
        self._top_correlations = self._get_top_correlations(num_correlations)

    def _get_headers(self):
        """
        Returns the headers for the data

        Returns:
            list of string representing the headers of the dataset.
        """
        return self._data.columns

    def _get_redundant_pairs(self):
        '''Get diagonal and lower triangular pairs of correlation matrix'''
        pairs_to_drop = set()
        for i in range(0, self._data.shape[1]):
            for j in range(0, i+1):
                pairs_to_drop.add((self._headers[i], self._headers[j]))
        return pairs_to_drop

    def _get_top_correlations(self, n: int):
        unstacked_corr = self._data.apply(
            lambda x: x.factorize()[0]).corr().abs().unstack()
        labels_to_drop = self._get_redundant_pairs()
        unstacked_corr = unstacked_corr.drop(
            labels=labels_to_drop).sort_values(ascending=False)
        return unstacked_corr[:n]

    @property
    def headers(self):
        return self._headers

    @property
    def top_correlations(self):
        return self._top_correlations

    @property
    def count(self):
        return len(self._data)

    @property
    def total_headers(self):
        return len(self._headers)

    @property
    def data(self):
        return self._data

    def get_mean(self, col: str):
        if col in self._headers and \
                np.issubdtype(self._data[col].dtype, np.number):
            return self._data[col].mean()
        return '-'

    def get_std(self, col: str):
        if col in self._headers and \
                np.issubdtype(self._data[col].dtype, np.number):
            return self._data[col].std()
        return '-'

    def get_min(self, col: str):
        if col in self._headers and \
                np.issubdtype(self._data[col].dtype, np.number):
            return self._data[col].min()
        return '-'

    def get_max(self, col: str):
        if col in self._headers and \
                np.issubdtype(self._data[col].dtype, np.number):
            return self._data[col].max()
        return '-'

    def get_median(self, col: str):
        if col in self._headers and \
                np.issubdtype(self._data[col].dtype, np.number):
            return self._data[col].median()
        return '-'

    def get_unique_count(self, col: str):
        if col in self._headers:
            return len(self._data[col].unique())
        return '-'

    def get_mode(self, col: str):
        if col in self._headers:
            return list(self._data[col].mode())[0]
        return '-'

    def get_mode_frequency(self, col: str):
        if col in self._headers:
            mode = self.get_mode(col)
            return self._data[col].value_counts()[mode]
        return '-'
