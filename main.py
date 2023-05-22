import colorama
import sys

import constants
from importers import DataImporter
from analyzers import Analyzer
from exporters import ConsoleExporter


colorama.init(autoreset=True)


if __name__ == '__main__':
    dataset_location = input('Enter the location of the dataset file: ')
    importer = DataImporter(dataset_location)

    if importer.import_status == constants.NOT_FOUND:
        sys.exit(1)
    else:
        dataset_analyzer = Analyzer(importer)
        print(f'\nHere are the details for the file: {importer.file}\n')

        console = ConsoleExporter(dataset_analyzer)
        console.export()

        print()
