'''Module with the content of all the pages of the section.
'''

from os.path import dirname
from os.path import exists
from src.utils import log
from src.lupo.compiler_lupo import fix_relative_paths

from settings import Settings
from page import Page


class Section:
    '''This class contains all pages of the section.

        Attributes:

        Methods:
           
    '''

    def __init__(
        self,
        section_id: int,
        name: str,
        markdown_file: str,
        settings: Settings):
        '''Constructor of the Section Class

            Parameters:

        '''
        self.section_id = section_id
        self.name = name
        self.pages = []
        self.videos = []

        self.settings = settings
        self.markdown_file = f"./{markdown_file}"

        print("markdown_file", markdown_file)
        if not exists(markdown_file):
            log(f"Check the toc file, the file {markdown_file} does not exists", "error")
        markdown_absolute_path = dirname(markdown_file).replace("\\", "/")
        print("markdown_absolute_path", markdown_absolute_path)
        # Open and Read the markdown content
        with open(markdown_file, "r", encoding="utf-8") as file:
            markdown_text = file.read()
            markdown_text = fix_relative_paths(markdown_text, markdown_absolute_path, settings.course_name)
        
        
    

    


    