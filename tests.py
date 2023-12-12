import unittest

from importers import DataImporter
from analyzers import Analyzer

import constants


class TestImporter(unittest.TestCase):

    def test_importer_with_no_file(self):
        input_file = './test_assets/not_available.txt'
        importer = DataImporter(input_file)
        self.assertEqual(importer.import_status,
                         constants.NOT_FOUND, "Should be not found")

    def test_import_with_empty_file(self):
        input_file = 'test_assets/dummy'
        importer = DataImporter(input_file)
        self.assertEqual(importer.import_status,
                         constants.EMPTY, "Should be empty")

    def test_import_with_correct_file(self):
        input_file = 'test_assets/realest.csv'
        importer = DataImporter(input_file)
        self.assertEqual(importer.import_status,
                         constants.IMPORTED, "Should be imported")

    def test_import_with_incorrect_file(self):
        input_file = 'test_assets/wrong.py'
        importer = DataImporter(input_file)
        self.assertEqual(importer.import_status,
                         constants.CANNOT_PARSE, "Should be unable to parse")


class TestAnalyzer(unittest.TestCase):
    IMPORTER = DataImporter('test_assets/realest.csv')
    ANALYZER = Analyzer(IMPORTER)

    def test_total_headers(self):
        expected = 9
        self.assertEqual(self.ANALYZER.total_headers,
                         expected, "There should be 9 headers")

    def test_unique_count_for_bedroom(self):
        expected = 7
        self.assertEqual(self.ANALYZER.get_unique_count('Bedroom'), expected,
                         'There should be 7 unique values of bedroom')


if __name__ == '__main__':
    unittest.main()
