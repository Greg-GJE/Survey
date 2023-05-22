import pandas as pd
import constants


class DataImporter:

    def __init__(self, file_location):
        self._dataframe = None
        self._import_status = self._import(file_location)

    def _import(self, file_location):
        try:
            self._dataframe = pd.read_csv(file_location)
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

    @property
    def headers(self):
        return self._headers

    @property
    def data(self):
        return self._data

    def _get_headers(self):
        return self._data.columns

    def _get_count(self):
        pass

    def _get_standard_deviation(self):
        pass

    def _get_median(self):
        pass

    def _get_mean(self):
        pass

    def analyze(self):
        pass


df = pd.read_csv('./annual-enterprise-survey-2021-financial-year-provisional-csv.csv')
print(df.columns)

print(f'Total entries: {len(df)}')


print(df.describe())

for column in df.columns:
    print(column)
    print(df[column].describe())


