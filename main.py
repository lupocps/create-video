''' Create Videos '''

from os import environ
#import requests
from io import StringIO
from src.lupo.user_verification import user_verification
from src.lupo.compiler_lupo import validate_yaml_file_details

from src.utils import read_toc


def main():
    ''' Main method '''
    output_builder = StringIO()

    # read environment variables
    toc = environ["INPUT_TOC"]
    github_actor = environ["GITHUB_ACTOR"]
    github_repository = environ["GITHUB_REPOSITORY"]

    # read toc
    if toc:
        yaml_dict = read_toc(toc, github_repository, output_builder)

    print("output_string after read toc: ", output_builder)
    is_final = ('final' in yaml_dict) and yaml_dict['final'] is True

    user_details = user_verification(is_final, github_actor, github_repository, output_builder)
    print("output_string after user_verification: ", output_builder)
    validate_yaml_file_details(yaml_dict)
    my_output = output_builder.getvalue()
    
    lines = my_output.split("\n")
    key_value_pairs = [line.split(":", 1) for line in lines if line.strip()]

    # Create the formatted output string
    formatted_output = "\n".join([f"{key.strip()}={value.strip()}" for key, value in key_value_pairs])

    
    with open(environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as file:
        print(f"myOutput={formatted_output}\n", file=file)
        





if __name__ == "__main__":
    main()
