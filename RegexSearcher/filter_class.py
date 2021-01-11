import csv
import re
import sys
import time
import PyPDF2
import pyinputplus as pyip
from pathlib import Path


class Filter:
    def __init__(self):
        self.filepath = None
        self.pattern = None
        self.output_dir = 'C:\\Users\\ponce\\Documents'

    def __str__(self):
        return f"A filter object to find matches"

    def handler(self):
        # Select function to apply based on file extension
        if '.txt' in self.filepath:
            self._find_matches_txt()
            self._output(self._find_matches_txt())
        elif '.csv' in self.filepath:
            self._find_matches_csv()
            self._output(self._find_matches_csv())
        elif '.pdf' in self.filepath:
            self._find_matches_pdf()
            self._output(self._find_matches_pdf())
        elif '.word' in self.filepath:
            self._find_matches_word()
            self._output(self._find_matches_word())

    def set_filepath(self):
        i = 0
        while i < 3:
            self.filepath = input("Select file: ")
            try:
                if Path(self.filepath).is_file():
                    break
                if i == 2:
                    print("File not found. Closing program...")
                    time.sleep(2)
                    sys.exit()
                else:
                    print("File not found, please try again")
                    i += 1
            except OSError:
                print("Character incorrect in filepath")
                i += 1

    def set_output_dir(self):
        i = 0
        while i < 3:
            self.filepath = input("Select output directory: ")
            try:
                if Path(self.filepath).is_dir():
                    break
                if i == 2:
                    print("Directory not found. Closing program...")
                    time.sleep(2)
                    sys.exit()
                else:
                    print("Directory not found, please try again")
                    # print(f"Attempts left: {5-(i+1)}")
                    i += 1
            except OSError:
                print("Character incorrect in filepath")
                i += 1

    def select_pattern(self):
        options = ['Email', 'Mobile phone', 'Url']
        choice = pyip.inputMenu(options, numbered=True, allowRegexes=['(1-4)'], limit=10)

        # Set pattern
        if options.index(choice) == 0:
            self.pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})')
        elif options.index(choice) == 1:
            self.pattern = re.compile(r'(6[0-9]{8})')
        elif options.index(choice) == 2:
            self.pattern = re.compile('''http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|
                                         (?:%[0-9a-fA-F][0-9a-fA-F]))+''', re.VERBOSE)

    # Find matches in a file.txt
    def _find_matches_txt(self):
        file = open(self.filepath, "r")
        matches = '\n'.join(re.findall(self.pattern, file.read()))
        file.close()
        return matches

    # Find matches in a file.csv
    def _find_matches_csv(self):
        file = open(self.filepath, "r")
        csv_reader = csv.reader(file)
        matches = [f'Line {row} - {", ".join(re.findall(self.pattern, str(row)))}' for row in csv_reader]
        file.close()
        return matches

    # Find matches in a file.pdf
    def _find_matches_pdf(self):
        file = open(self.filepath, "rb")
        pdf_reader = PyPDF2.PdfFileReader(file)
        matches = {page: re.findall(self.pattern, pdf_reader.getPage(page).extractText())
                   for page in range(0, pdf_reader.numPages)}
        file.close()
        return matches

    # TODO Find matches in a file.word
    def _find_matches_word(self):
        pass

    def _output(self, matches):
        output_filename = f'results_{Path(self.filepath).stem}_{time.strftime("%H%M%S")}.txt'
        output_path = f'{self.output_dir}\\{output_filename}'
        results = open(output_path, 'a')

        # Write results based on file
        try:
            if '.txt' in self.filepath:
                results.write(f'{matches}\n')
            elif '.csv' in self.filepath:
                for match in matches:
                    results.write(f'{match}\n')
            elif '.pdf' in self.filepath:
                for key in matches:
                    results.write(f'Page number {str(key)} - {", ".join(matches.get(key))}\n')
        except FileExistsError as e:
            print(f"File already exists {e}")
        finally:
            print("Process successfully")
            time.sleep(1)
            print(f"Find results in: {output_path}")
