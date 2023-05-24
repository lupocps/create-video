''' Printer '''

import os

def print_info():
    '''Prints important information'''

    toc = os.environ["INPUT_TOC"]

    if toc:
        with open(toc, 'r', encoding='utf-8') as toc_file:
            print(toc_file.read())

    github_actor = os.environ["GITHUB_ACTOR"]
    github_repository = os.environ["GITHUB_REPOSITORY"]
    print(f"Actor: {github_actor}, Repository: {github_repository}")
