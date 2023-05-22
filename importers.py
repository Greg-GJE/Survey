import pandas as pd

import constants

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
