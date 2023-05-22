from colorama import Fore, Style

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
                f' {"Max":10} | {"Min":10} |' +
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
            fp.write(f'Total entries: {self._analyzer.count}\n')
            fp.write(f'Total Columns: {self._analyzer.total_headers}\n')

            fp.write("\nOverview of each column\n\n")

            fp.write( '|--------------------------------|----------------------|---------' +
                    '---|------------|------------|------------|------------|-----------------|---' +
                    '--------------|\n')

            fp.write( f'| {"Column":30} | {"Standard Deviation":20} |' +
                    f' {"Max":10} | {"Min":10} |' +
                    f' {"Mean":10} | {"Median":10} | {"Mode":10} |'
                    f' {"Mode Frequency":15} | {"Unique Count":15} |\n')

            fp.write( '|--------------------------------|----------------------|---'
                    + '---------|------'
                    + '------|------------|------------|------------|-----------------|-------'
                    + '----------|\n')

            for header in self._analyzer.headers:
                standard_deviation = self._analyzer.get_std(header)
                max_val = self._analyzer.get_max(header)
                min_val = self._analyzer.get_min(header)
                mean_val = self._analyzer.get_mean(header)
                median_val = self._analyzer.get_median(header)
                mode_val = self._analyzer.get_mode(header)
                mode_freq_val = self._analyzer.get_mode_frequency(header)
                unique_val = self._analyzer.get_unique_count(header)

                fp.write(  f'| {header:30} |'
                        + f' {standard_deviation:<20.2f} |'
                        + f' {max_val:<10} |'
                        + f' {min_val:<10}'
                        + f' | {mean_val:<10.2f}'
                        + f' | {median_val:<10} |'
                        + f' {mode_val:<10} |'
                        + f' {mode_freq_val:<15} |'
                        + f' {unique_val:<15} |\n' )
                fp.write( '|--------------------------------|--------------------'
                        + '--|------------|------------|-----------'
                        + '-|------------|------------|-----------------|-----------------|\n')

            fp.write('\nTop Correlations\n')
            fp.write("-------------------\n\n")
            correlation_results = self._analyzer.top_correlations
            for col_pairs, value in correlation_results.items():
                (column1, column2) = col_pairs
                fp.write(f'{column1:20}{column2:20}{value}\n')
