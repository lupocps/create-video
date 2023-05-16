''' Create Videos '''

import os
import requests


def main():
    ''' Main method '''
    my_input = os.environ["INPUT_MYINPUT"]
    my_output = f"Hello {my_input}"

    print(f"::set-output name=my_output::{my_output}")


if __name__ == "__main__":
    main()
