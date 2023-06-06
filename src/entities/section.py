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
from src.lupo.compiler_lupo import validate_narration
from src.lupo.compiler_lupo import extract_content_audio_compiler
from src.entities.settings import Settings
from src.entities.page import Page


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
        if settings.trailer_mode:
            self.tts_components = settings.tts_components[id-1]
        else:
            self.tts_components = settings.tts_components


        if not exists(markdown_file):
            log(f"Check the toc file, the file {markdown_file} does not exists", "error")

        markdown_absolute_path = dirname(markdown_file).replace("\\", "/")

        # Open and Read the markdown content
        with open(markdown_file, "r", encoding="utf-8") as file:
            markdown_text = file.read()

            markdown_text = fix_relative_paths(markdown_text, markdown_absolute_path, settings.course_name) # Problem
        
        markdown_slides = [slide for slide in re.split(r"\-\-\-\s?\n", markdown_text) if slide.strip() != '']

        markdown_header = markdown_slides[0]

        markdown_header, current_theme_file = validate_header(markdown_header, settings.themes, self.name)
        page_id = 1
        for page in markdown_slides[1:]:

            content, audio_note = extract_content_audio_compiler(page, page_id, self.name)
            content = validate_md_content(content, page_id, self.name, current_theme_file)

            if "https://mlgstorageaccount.blob.core.windows.net/docs/media/silence.mp3" != audio_note:
                audio_notes = validate_narration(settings.tts_components, audio_note, page_id, self.name)

            page = Page(page_id=page_id, marp_header=markdown_header, markdown_text=content,
                        audio_notes=audio_notes, settings=settings)
            page_id += 1
    
            page.source_md = markdown_absolute_path

            self.pages.append(page)


    def generate_video(self) -> str:
        '''Generate a video with the content of all the pages of the section.

            Return:
                str: Path of the video generated
        '''
        for page in self.pages:
          #  page.generate_path()
            audio_notes = page.generate_audio_notes(self.tts_components)
            source = page.generate_source()
            video = page.generate_video(audio_notes, source)
            #video_only_file = page.generate_video()
 
