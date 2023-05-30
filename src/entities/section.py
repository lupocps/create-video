'''Module with the content of all the pages of the section.
'''

import os
import re
from os.path import dirname
from os.path import exists
from src.utils import log

from src.lupo.compiler_lupo import fix_relative_paths
from src.lupo.compiler_lupo import validate_header
from src.lupo.compiler_lupo import validate_md_content
from src.lupo.compiler_lupo import extract_content_audio_compiler
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
            #print("The text is", markdown_text)
        
        markdown_slides = [slide for slide in re.split(r"\-\-\-\s?\n", markdown_text) if slide.strip() != '']
        print("the markdown slides are", markdown_slides)

        markdown_header = markdown_slides[0]

        print("markdown_header", markdown_header)
        markdown_header, current_theme_file = validate_header(markdown_header, settings.themes, self.name)
        #print("markdown_header_new", markdown_header)


        page_id = 1
        for page in markdown_slides[1:]:
            content, audio_note = extract_content_audio_compiler(page, page_id, self.name)
            print("markdown_text", content)
            print("audio_note", audio_note)
            content = validate_md_content(content, page_id, self.name, current_theme_file)
            print("markdown_text_before_validation", content)
            if "silence.mp3" in audio_note:
                #Check this
                print("current_directory in silence page", current_directory)
                current_directory = os.getcwd().replace("\\", "/")
                silence_path = f"{current_directory}/{audio_note}"
                print("silence_path", silence_path)
                markdown_text_validate += f"<!--{silence_path}-->"
                print("markdown_text_validate", markdown_text_validate)
            else:
               # markdown_text_validate += validate_narration(settings.tts_components, audio_note, settings.root_folder, page_id, section_file_name)
                print("hello")
          #  if settings.trailer_mode:
           #     break
            markdown_text_validate += "\n\n---\n\n"
            page_id += 1


    
