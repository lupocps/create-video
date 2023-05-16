''' Create Videos '''

import os
import requests


def main():
    ''' Main method '''
    my_input = os.environ["INPUT_MYINPUT"]
    my_output = f"Hello {my_input}"

    github_actor = os.environ["GITHUB_ACTOR"]
    github_repository = os.environ["GITHUB_REPOSITORY"]
    print(f"Actor: {github_actor}, Repository: {github_repository}")

    my_input = os.environ["INPUT_MYINPUT"]

    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as file:
        print(f"myOutput={my_output}\n", file=file)


if __name__ == "__main__":
    main()
