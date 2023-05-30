'''Module with the content of all the pages of the section.
'''

import re
from os.path import dirname
from os.path import exists
from src.utils import log

from src.lupo.compiler_lupo import fix_relative_paths
from src.entities.settings import Settings
#from page import Page


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
            # SOLO REVISA EL CONTENIDO?, NO, TAMBIEN REVISA HEADER
            markdown_text = fix_relative_paths(markdown_text, markdown_absolute_path, settings.course_name)
            print("The text is", markdown_text)
        
        markdown_slides = [slide for slide in re.split(r"\-\-\-\s?\n", markdown_text) if slide.strip() != '']
        print("the markdown slides are", markdown_slides)

        markdown_header = markdown_slides[1]

        print("markdown_header", markdown_header)
       # markdown_header, current_theme_file = validate_header(markdown_header, settings.themes, settings.mail, self.name)
        #print("markdown_header_new", markdown_header)


        page_id = 1
        for page in markdown_slides[1:]:
            result = re.search(r"((.|\n)*)<!--\s*((.|\n)*)\s*-->", page)
            markdown_text = result.group(1)
            audio_note = result.group(3)
            print("markdown_text", markdown_text)
            print("audio_note", audio_note)
          #  content, audio_note = extract_content_audio_compiler(page, page_id, section_file_name) 
    


    
