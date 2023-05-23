import colorama
import sys

import constants
from importers import DataImporter
from analyzers import Analyzer
from exporters import ConsoleExporter, FileExporter


colorama.init(autoreset=True)


if __name__ == '__main__':
    print('Importing the real estate data')
    dataset_location = './realest.csv'
    importer = DataImporter(dataset_location)

    if importer.import_status != constants.IMPORTED:
        sys.exit(1)
    else:
        dataset_analyzer = Analyzer(importer)
        print(f'\nHere are the details for the file: {importer.file}\n')

        console = ConsoleExporter(dataset_analyzer)
        console.export()

        print()
        choice = input('Do you want to export the data (Y/N)?')

        # if the choice is either y or yes
        if choice.lower() in ['y', 'yes']:
            output_file_loc = input('Enter the location of the output file: ')
            file_exporter = FileExporter(dataset_analyzer, output_file_loc)
            file_exporter.export()
            print(f'Successfully exported to file {output_file_loc}')

        print('\nThanks for trying out the application.')

