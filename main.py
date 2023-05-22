import pandas as pd
import numpy as np
import constants
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

class DataImporter:

    def __init__(self, file_location):
        self._file = file_location
        self._dataframe = None
        self._import_status = self._import()

    def _import(self):
        try:
            self._dataframe = pd.read_csv(self._file).dropna()
            return constants.IMPORTED
        except FileNotFoundError:
            print("The requested file could not be found!")
            return constants.NOT_FOUND

    @property
    def file(self):
        return self._file

    @property
    def import_status(self):
        return self._import_status

    @property
    def data(self):
        return self._dataframe


class Analyzer:
    def __init__(self, importer, num_correlations = 5) -> None:
        self._data = importer.data
        self._headers = self._get_headers()
        self._top_correlations = self._get_top_correlations(num_correlations)

    def _get_headers(self):
        return self._data.columns

    def _get_redundant_pairs(self):
        '''Get diagonal and lower triangular pairs of correlation matrix'''
        pairs_to_drop = set()
        for i in range(0, self._data.shape[1]):
            for j in range(0, i+1):
                pairs_to_drop.add((self._headers[i], self._headers[j]))
        return pairs_to_drop

    def _get_top_correlations(self, n: int):
        unstacked_corr = self._data.apply(lambda x: x.factorize()[0]).corr().abs().unstack()
        labels_to_drop = self._get_redundant_pairs()
        unstacked_corr = unstacked_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
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
        if col in self._headers and np.issubdtype(self._data[col].dtype, np.number):
            return self._data[col].mean()
        return '-'

    def get_std(self, col: str):
        if col in self._headers and np.issubdtype(self._data[col].dtype, np.number):
            return self._data[col].std()
        return '-'

    def get_min(self, col: str):
        if col in self._headers and np.issubdtype(self._data[col].dtype, np.number):
            return self._data[col].min()
        return '-'

    def get_max(self, col: str):
        if col in self._headers and np.issubdtype(self._data[col].dtype, np.number):
            return self._data[col].max()
        return '-'

    def get_median(self, col: str):
        if col in self._headers and np.issubdtype(self._data[col].dtype, np.number):
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



class DataExporter:
    def __init__(self, analyzer) -> None:
        self._analyzer = analyzer

    def export(self):
        pass


class ConsoleExporter(DataExporter):

    def export(self):
        print(f'Total entries: {self._analyzer.count}')
        print(f'Total Columns: {self._analyzer.total_headers}')

        print("\nOverview of each column\n")

        print(  Fore.YELLOW + '|--------------------------------|----------------------|---------' +
                '---|------------|------------|------------|------------|-----------------|---' +
                '--------------|')

        print(  Fore.YELLOW + f'| {"Column":30} | {"Standard Deviation":20} |' +
                ' {"Max":10} | {"Min":10} |' +
                f' {"Mean":10} | {"Median":10} | {"Mode":10} |'
                f' {"Mode Frequency":15} | {"Unique Count":15} |')

        print(  Fore.YELLOW + '|--------------------------------|----------------------|---'
                + '---------|------'
                + '------|------------|------------|------------|-----------------|-------'
                + '----------|')

        for header in self._analyzer.headers:
            standard_deviation = self._analyzer.get_std(header)
            max_val = self._analyzer.get_max(header)
            min_val = self._analyzer.get_min(header)
            mean_val = self._analyzer.get_mean(header)
            median_val = self._analyzer.get_median(header)
            mode_val = self._analyzer.get_mode(header)
            mode_freq_val = self._analyzer.get_mode_frequency(header)
            unique_val = self._analyzer.get_unique_count(header)

            print(  f'{Fore.YELLOW}| {Style.RESET_ALL}{header:30} {Fore.YELLOW}|'
                    + f' {Style.RESET_ALL}{standard_deviation:<20.2f} {Fore.YELLOW}|'
                    + f' {Style.RESET_ALL}{max_val:<10} {Fore.YELLOW}|'
                    + f' {Style.RESET_ALL}{min_val:<10}'
                    + f' {Fore.YELLOW}| {Style.RESET_ALL}{mean_val:<10.2f}'
                    + f' {Fore.YELLOW}| {Style.RESET_ALL}{median_val:<10} {Fore.YELLOW}|'
                    + f' {Style.RESET_ALL}{mode_val:<10} {Fore.YELLOW}|'
                    + f' {Style.RESET_ALL}{mode_freq_val:<15} {Fore.YELLOW}|'
                    + f' {Style.RESET_ALL}{unique_val:<15} {Fore.YELLOW}|' )
            print(  Fore.YELLOW + '|--------------------------------|--------------------'
                    + '--|------------|------------|-----------'
                    + '-|------------|------------|-----------------|-----------------|')

        print('\nTop Correlations')
        print("-------------------\n")
        correlation_results = self._analyzer.top_correlations
        for col_pairs, value in correlation_results.items():
            (column1, column2) = col_pairs
            print(f'{column1:20}{column2:20}{value}')


class FileExporter(DataExporter):
    def __init__(self, analyzer, output_file) -> None:
        super().__init__(analyzer)
        self._out = output_file

    def export(self):
        with open(self._out, 'w', encoding='utf-8') as fp:
            pass


if __name__ == '__main__':
    dataset_location = input('Enter the location of the dataset file: ')
    importer = DataImporter(dataset_location)

    if importer.import_status == constants.NOT_FOUND:
        print('The requested file could not be found')
    else:
        dataset_analyzer = Analyzer(importer)
        print(f'\nHere are the details for the file: {importer.file}\n')

        console = ConsoleExporter(dataset_analyzer)
        console.export()

        print()









# with open('hello.txt', 'w') as op:

#     op.write(str(m.iloc[:, :]))
