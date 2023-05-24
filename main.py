''' Create Videos '''

from os import environ
#import requests

from src.lupo.user_verification import user_verification
from src.lupo.compiler_lupo import validate_yaml_file_details

from src.utils import read_toc


def main():
    ''' Main method '''
    
    my_output = "TEST"


    # read environment variables
    toc = environ["INPUT_TOC"]
    github_actor = environ["GITHUB_ACTOR"]
    github_repository = environ["GITHUB_REPOSITORY"]

    # read toc
    if toc:
        yaml_dict = read_toc(toc, github_repository)

    is_final = ('final' in yaml_dict) and yaml_dict['final'] is True

    user_details = user_verification(is_final, github_actor, github_repository)

    validate_yaml_file_details(yaml_dict)
    my_output += f"\n{user_details}\n"
    print(my_output)
    print(environ['GITHUB_OUTPUT'])
    with open(environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as file:
        print("Enter")
        print(f"myOutput={my_output}\n", file=file)





if __name__ == "__main__":
    main()
