''' Create Videos '''

import os
import requests


def main():
    ''' Main method '''
    toc = os.environ["INPUT_TOC"]

    if toc:
        with open(toc, 'r', encoding='utf-8') as toc_file:
            print(toc_file.read())

    github_actor = os.environ["GITHUB_ACTOR"]
    github_repository = os.environ["GITHUB_REPOSITORY"]
    print(f"Actor: {github_actor}, Repository: {github_repository}")

    my_output = f"toc {toc}"

    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as file:
        print(f"myOutput={my_output}\n", file=file)


if __name__ == "__main__":
    main()
