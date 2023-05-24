''' Create Videos '''

import os
#import requests

from src.lupo.user_verification import user_verification



def main():
    ''' Main method '''

    toc = os.environ["INPUT_TOC"]

    user_verification(toc)


if __name__ == "__main__":
    main()
