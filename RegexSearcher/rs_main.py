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
def output_menu():
    i = 0
    while i < 5:
        options = input(f"Select output folder? Y/N\nDefault: {filter_obj.output_dir}\n").upper()
        if i == 4:
            break
        if options == 'Y':
            filter_obj.set_output_dir()
        elif options == 'N':
            break
        else:
            print("Incorrect option. Please, try again")




# Main execution
if __name__ == '__main__':
    print("\n")
    print("------------------------Regex Searcher------------------------")
    print()
    filter_obj = fc.Filter()
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
