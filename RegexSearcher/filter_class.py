import csv
import re
import sys
import os
import time
import PyPDF2
import pyinputplus as pyip
from pathlib import Path


class Filter:
    def __init__(self):
        self.filepath = None
        self.pattern = None
        self.matches = []
        self.outputDir = f'C:\\Users\\{os.getlogin()}\\Documents'

    def __str__(self):
        return f"A filter object to find matches"

    def set_filepath(self, n=3):
        i = 0
        while i < n:
            try:
                self.filepath = input("Select file: ").strip()
                if Path(self.filepath).is_file():
                    break
                elif i == n - 1:
                    print("File not found. Closing program...")
                    time.sleep(2)
                    sys.exit()
                else:
                    print("File not found, please try again")
                    i += 1
            except OSError:
                print("The filename, directory name, or volume label syntax is incorrect")
                i += 1

    def set_outputDir(self,  n=3):
        i = 0
        while i < n:
            try:
                self.filepath = input("Select output directory: ").strip()
                if Path(self.filepath).is_dir():
                    break
                elif i == n - 1:
                    print("Directory not found. Closing program...")
                    time.sleep(2)
                    sys.exit()
                else:
                    print("Directory not found, please try again")
                    i += 1
            except OSError:
                print("The filename, directory name, or volume label syntax is incorrect")
                i += 1

    def handler(self):
        # Open file:
        try:
            file = open(self.filepath, "r", encoding="utf8")
            # Find matches:
            if '.txt' in self.filepath:
                self.matches = '\n'.join(re.findall(self.pattern, file.read()))
            elif '.csv' in self.filepath:
                csv_reader = csv.reader(file)
                self.matches = [f'Line {row} - {", ".join(re.findall(self.pattern, str(row)))}' for row in csv_reader]
            elif '.pdf' in self.filepath:
                pdf_reader = PyPDF2.PdfFileReader(file)
                self.matches = {page: re.findall(self.pattern, pdf_reader.getPage(page).extractText())
                                for page in range(0, pdf_reader.numPages)}
            elif '.docx' in self.filepath:
                pass
            # Write output
            self._output(self.matches)
            file.close()
        except PermissionError:
            print(f"Permission denied: can't open file {self.filepath}")
        except UnicodeDecodeError:
            print("Encode error. Try different encoding")

    def select_pattern(self):
        options = ['Email', 'Mobile phone', 'Url']
        choice = pyip.inputMenu(options, numbered=True, allowRegexes=['(1-3)'], limit=10)
        # Set pattern
        if options.index(choice) == 0:
            self.pattern = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})')
        elif options.index(choice) == 1:
            self.pattern = re.compile(r'(6[0-9]{8})')
        elif options.index(choice) == 2:
            self.pattern = re.compile('''http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|
                                         (?:%[0-9a-fA-F][0-9a-fA-F]))+''', re.VERBOSE)

    def _output(self, matches):
        output_filename = f'results_{Path(self.filepath).stem}_{time.strftime("%H%M%S")}.txt'
        output_path = f'{self.outputDir}\\{output_filename}'
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
