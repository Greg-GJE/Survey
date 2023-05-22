import pandas as pd
import numpy as np
import constants
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

class DataImporter:

    def __init__(self, file_location):
        self._dataframe = None
        self._import_status = self._import(file_location)

    def _import(self, file_location):
        try:
            self._dataframe = pd.read_csv(file_location).dropna()
            return constants.IMPORTED
        except FileNotFoundError:
            print("The requested file could not be found!")
            return constants.NOT_FOUND

    @property
    def data(self):
        return self._dataframe


class Analyzer:
    def __init__(self, importer) -> None:
        self._data = importer.data
        self._headers = self._get_headers()
        self._mean = None
        self._median = None
        self._mode = None
        self._correlation = None

    @property
    def headers(self):
        return self._headers

    @property
    def data(self):
        return self._data

    def _get_headers(self):
        return self._data.columns

    def analyze(self):
        pass



df = pd.read_csv('./realest.csv')
# print(df.columns)

class DataExporter:
    def __init__(self, data, output_file) -> None:
        self._out = output_file
        self._data = data

    def export(self):
        with open(self._out, 'w', encoding='utf-8') as fp:
            pass




print(f'Total entries: {len(df)}')
print(f'Total Columns: {len(df.columns)}')

print("\nOverview of each column\n")

print(Fore.YELLOW + '|--------------------------------|----------------------|------------|------------|------------|------------|------------|-----------------|-----------------|')
print(Fore.YELLOW + f'| {"Column":30} | {"Standard Deviation":20} | {"Max":10} | {"Min":10} | {"Mean":10} | {"Median":10} | {"Mode":10} | {"Mode Frequency":15} | {"Unique Count":15} |')
print(Fore.YELLOW + '|--------------------------------|----------------------|------------|------------|------------|------------|------------|-----------------|-----------------|')

for column in df.columns:
    standard_deviation = '-'
    max_val = '-'
    min_val = '-'
    mean_val = '-'
    median_val = '-'
    mode_val = '-'
    mode_freq_val = '-'

    unique_val = len(df[column].unique())

    if (np.issubdtype(df[column].dtype, np.number)):
        standard_deviation = df[column].std()
        max_val = df[column].max()
        min_val = df[column].min()
        mean_val = df[column].mean()
        median_val = df[column].median()

    modes = list(df[column].mode())

    if len(modes) > 0:
        mode_val = modes[0]
        mode_freq_val = df[column].value_counts()[mode_val]


    print(f'{Fore.YELLOW}| {Style.RESET_ALL}{column:30} {Fore.YELLOW}| {Style.RESET_ALL}{standard_deviation:<20.2f} {Fore.YELLOW}| {Style.RESET_ALL}{max_val:<10} {Fore.YELLOW}| {Style.RESET_ALL}{min_val:<10} {Fore.YELLOW}| {Style.RESET_ALL}{mean_val:<10.2f} {Fore.YELLOW}| {Style.RESET_ALL}{median_val:<10} {Fore.YELLOW}| {Style.RESET_ALL}{mode_val:<10} {Fore.YELLOW}| {Style.RESET_ALL}{mode_freq_val:<15} {Fore.YELLOW}| {Style.RESET_ALL}{unique_val:<15} {Fore.YELLOW}|')
    print(Fore.YELLOW + '|--------------------------------|----------------------|------------|------------|------------|------------|------------|-----------------|-----------------|')


def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_correlations(df, n=5):
    au_corr = df.apply(lambda x: x.factorize()[0]).corr(method='pearson').abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[:10]

print('\nTop Correlations\n')
print("----------------")
res = get_top_correlations(df)
for key, value in res.items():
    (column1, column2) = key
    print(f'{column1:20}{column2:20}{value}')

# with open('hello.txt', 'w') as op:

#     op.write(str(m.iloc[:, :]))
