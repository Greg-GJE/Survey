import colorama
import requests
import sys

import constants
from importers import DataImporter
from analyzers import Analyzer
from exporters import ConsoleExporter, FileExporter

colorama.init(autoreset=True)


if __name__ == '__main__':

    url = input('Enter the URL for the dataset file (preferably csv): ')
    file_name = input('Enter the name of the file to save: ')

    try:
        r = requests.get(url, allow_redirects=True, timeout=20)
        content_type = r.headers.get('Content-Type')

        if 'text/csv' in content_type:
            with open(file_name, 'wb') as fw:
                fw.write(r.content)

            print('Importing the real estate data')
            dataset_location = file_name
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
        else:
            print('The given format of the response is not a csv file! Please give appropriate data!')

    except requests.exceptions.MissingSchema:
        print('Invalid URL! Please enter correct url and try again.')
        sys.exit(1)

