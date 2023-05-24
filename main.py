''' Create Videos '''

import os
#import requests
from src.printer import print_info


def main():
    ''' Main method '''

    print_info()

    toc = os.environ["INPUT_TOC"]
    my_output = f"toc {toc}"

    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as file:
        print(f"myOutput={my_output}\n", file=file)


if __name__ == "__main__":
    main()
