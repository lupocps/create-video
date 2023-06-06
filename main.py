''' Create Videos '''

from os import environ
#import requests

#from src.lupo.user_verification import user_verification
from src.lupo.compiler_lupo import validate_yaml_file_details
from src.lupo.course_generation import generate_course
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

  #  user_details = user_verification(is_final)

    ##COMPILER DETAILS
    settings = validate_yaml_file_details(yaml_dict)

    ##COMPILER BODY
    # Create course objects
    log('[1/2] Validation. Starting slides validation.', 'info')
    course = Course(settings)
    log('Validation complete.', 'info')


    # Generate one video per chapter
    log('[2/2] Generation. Starting Content Generation.', 'info')
    azure_folder = f"{settings.course_name}/{settings.course_version}/{settings.course_uuid}"


    course_data = {
        "Chapters" : []
    }


    course_data = generate_course(course.chapters, settings, azure_folder, course_data)




    with open("./app.log", "r", encoding='utf-8') as file:
        my_output = file.read()
    
    print("MY OUTPUT", my_output)

    toc_output = f"toc {toc}"
    with open(environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as file:
        print(f"myOutput={toc_output}\n", file=file)
        


if __name__ == "__main__":
    main()
