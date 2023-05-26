'''Module with the content of all the pages of the section.
'''
import re
from os.path import dirname
from os.path import exists
#from os.path import normpath
#from os.path import join
#from os.path import basename
from src.utils import log
#from coursecreator.utils import MARP_DIRECTIVES
#from coursecreator.video import concatenate_video_and_audio_notes
#from coursecreator.video import concatenate_videos_files
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
        
        
        
        
        # Split marp markdown in Slides using '---'
       # markdown_slides = [slide for slide in re.split(r"\-\-\-\s?\n", markdown_text) if slide.strip() != '']
       # page_id = 1
       # for page in markdown_slides[1:]:
        #    result = re.search(r"((.|\n)*)<!--\s*((.|\n)*)\s*-->", page)
        #    markdown_text = result.group(1)
        #    audio_note = result.group(3)
       #    page = Page(id=page_id, marp_header=f"---\n{markdown_slides[0]}\n---\n", markdown_text=markdown_text,
        #                audio_notes=audio_note, settings=settings)

        #    page.source_md = markdown_absolute_path

         #   self.pages.append(page)
        #    page_id += 1


    # def generate_video(self) -> str:
    #     '''Generate a video with the content of all the pages of the section.

    #         Return:
    #             str: Path of the video generated
    #     '''

    #     for page in self.pages:
    #         page.generate_path()
    #         audio_notes = page.generate_audio_notes(self.settings.tts_components)
    #         video_only_file = page.generate_video()
    #         video = concatenate_video_and_audio_notes(
    #             video_only_file,
    #             audio_notes,
    #             f"{page.get_output_path()}/{page.id}",
    #             draft= not self.settings.final, #to change to draft
    #             is_console_application = True
    #         )
    #         self.videos.append(video)

    #     concatenate_video, time = concatenate_videos_files(self.videos, output_path=self.output_directory)
    #     self.settings.measure_timing.add_time(time)
    #     self.settings.measure_timing.add_video_amount()

    #     return concatenate_video


    


    
