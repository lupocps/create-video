''' Create Videos '''

from os import environ
#import requests

from src.lupo.user_verification import user_verification
from src.lupo.compiler_lupo import validate_yaml_file_details

from src.utils import read_toc
from src.utils import log
from src.entities.course import Course

def main():
    ''' Main method '''

    toc = environ["INPUT_TOC"]
    

    # read toc
    if toc:
        yaml_dict = read_toc(toc)

    is_final = ('final' in yaml_dict) and yaml_dict['final'] is True

   # user_details = user_verification(is_final)


    #COMPILER
    #DETAILS
    settings = validate_yaml_file_details(yaml_dict)

    print("settings", settings)
















    with open("./app.log", "r", encoding='utf-8') as file:
        my_output = file.read()
    
    print(my_output)

    toc_output = f"toc {toc}"
    with open(environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as file:
        print(f"myOutput={toc_output}\n", file=file)
        




if __name__ == "__main__":
    main()
