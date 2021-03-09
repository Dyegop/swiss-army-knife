"""
Documentation (pending)
...
"""

import time
import sys
import filter_class as fc


# Main menu
def main_menu():
    while True:
        print("Menu:")
        options = input("1. Enter c to continue\n2. Press ENTER to exit\n")
        if options == "":
            # Exit
            print("Closing program...")
            time.sleep(2)
            sys.exit()
        elif options.upper() == "C":
            # Select file
            filter_obj.set_filepath()
            break
        else:
            print("Please, try again")


# Output menu
def output_menu(n=3):
    i = 0
    while i < n:
        options = input(f"Select output directory? Y/N\nDefault: {filter_obj.outputDir}\n").upper()
        if options == 'Y':
            filter_obj.set_outputDir()
            break
        elif options == 'N':
            break
        else:
            if i == n-1:
                print("Too many incorrect options, using default output directory")
            else:
                print("Incorrect option. Please, try again")




# Main execution
if __name__ == '__main__':
    print("\n")
    print("------------------------Regex Searcher------------------------")
    print()
    filter_obj = fc.Filter()
    # print(filter_obj.__str__())
    time.sleep(2)

    while True:
        main_menu()
        time.sleep(1)
        output_menu()
        time.sleep(1)

        # Select pattern to match
        filter_obj.select_pattern()
        time.sleep(1)

        # Find matches and export to file.txt
        filter_obj.handler()
        print("\n")
        time.sleep(2)
