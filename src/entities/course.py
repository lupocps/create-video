'''Module with all the chapters of the course
'''
#import os

from settings import Settings
from chapter import Chapter
from src.utils import log
from src.lupo.compiler_lupo import slugify
from src.lupo.compiler_lupo import is_path_creatable

class Course:
    ''' This class contains all the chapters of the course.

        Attributes:



    '''
    def __init__(self, settings:Settings):
        '''The constructor for Course class.
            
            Parameters:
                settings (Settings): Object with the information for the attributes of this class
        '''

        self.chapters = []
        self.name = settings.course_name
       
        chapter_id = 1
        ## START THE STRUCTURE COMPILER
        if "chapters" in settings.yaml_dict:
            for chapter in settings.yaml_dict['chapters']:
                if "sections" in  chapter and "name" in chapter:
                    if not is_path_creatable(str(chapter['name'])):
                        log(f"Special characters in folder {chapter['name']} are not allowed .", 'warning')
                    chapter_name = slugify(chapter['name'])
                    self.chapters.append(
                        Chapter(
                            chapter_id = chapter_id,
                            name = chapter_name, 
                            yml_sections = chapter["sections"],
                            settings = settings
                        )
                    )
                    chapter_id += 1
                else:
                    log("The 'sections' or 'name' key is not found in one chapter", "error")
        else:
            log("The 'chapters' key is not found", "error")
        print("chapters", self.chapters)

    # def get_logs(self) -> str:
    #     '''Get the log file.

    #         Return:
    #             str: The path where the log file are located
    #     '''
    #     logs = os.path.abspath("./app.log").replace("\\", "/")
    #     return logs
