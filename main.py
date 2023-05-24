''' Create Videos '''

from os import environ
#import requests

from src.lupo.user_verification import user_verification
from src.lupo.compiler_lupo import validate_yaml_file_details

from src.utils import read_toc


def main():
    ''' Main method '''

    # read environment variables
    toc = environ["INPUT_TOC"]
    github_actor = environ["GITHUB_ACTOR"]
    github_repository = environ["GITHUB_REPOSITORY"]

    # read toc
    if toc:
        yaml_dict = read_toc(toc, github_repository)

    is_final = ('final' in yaml_dict) and yaml_dict['final'] is True
    print(is_final)

    user_details = user_verification(is_final, github_actor, github_repository)
    print(user_details)

    validate_yaml_file_details(yaml_dict)






if __name__ == "__main__":
    main()
