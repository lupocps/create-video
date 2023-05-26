'''Module with the content and audio notes of the page
'''
import re
from settings import Settings
#from coursecreator.utils import generate_directories
#from coursecreator.marp import generate_image
#from coursecreator.video import download_video
#from coursecreator.video import create_video
#from entities.tts_components import TTSComponents
#from entities.audio_note import AudioNote


class Page:
    '''This class contains all the content and audio notes of the page

        Attributes:


        Methods:

    '''

    def __init__(
        self,
        page_id: int,
        marp_header: str,
        markdown_text: str,
        audio_notes: list,
        settings: Settings):
        '''The constructor of the Page class.

            Parameters:

        '''
        self.page_id = page_id
        self.marp_header = marp_header
        self.markdown_text = markdown_text
        self.audio_notes = audio_notes
        self.settings = settings
        self.source_md = ""
        markdown_source_notes = re.sub(r'<mstts:express-as style="[^"]*">(.*?)<\/mstts:express-as>', r'\1', audio_notes)
        self.source_audio_notes = markdown_source_notes



    # def generate_image(self) -> str:
    #     '''Generates a slide image from markdown content using marp.

    #         Return:
    #              str : generated file path
    #     '''
    #     marp_text = f"{self.marp_header}\n{self.markdown_text}"
    #     output = generate_image(
    #         marp_text, self.settings.themes, self.output_directory)

    #     return output


    # def get_output_path(self) -> str:
    #     '''Get a path of the page
    #     '''
    #     return self.output_directory


    # def generate_path(self):
    #     '''Generate the directory path
    #     '''
    #     generate_directories(self.output_directory)

    # def generate_audio_notes(self, tts_components: TTSComponents) -> list:
    #     '''Converts each audio line to a AudioNote object.

    #         Return:
    #             list : AudioNote objects array
    #     '''
  
        
    #     audio_notes = [] 
    #     if ('silences/silence.mp3' in self.audio_notes) or (self.audio_notes == ''):
    #         return self.audio_notes

    #     regex_with_time = r'<mstts:express-as style=("([^"]+)")>\(\((\d+(?:,\s*\d+)*)\)\)\s*(.*?)<\/mstts:express-as>'
    #     regex_no_time = r'<mstts:express-as style=("([^"]+)")>\s*(.*?)<\/mstts:express-as>'
    #     has_time = re.search(
    #         r'\(\(', self.audio_notes, re.MULTILINE)  # Has time
        
    #     if has_time:
    #         for i, line in enumerate(self.audio_notes.split('\n')):
    #             if len(line) > 1:
    #                 audio_note_result_with_time = re.search(regex_with_time, line)
    #                 if  audio_note_result_with_time is None:
    #                     audio_note_result = re.search(regex_no_time, line)
    #                     audio_notes.append(
    #                         AudioNote(text=audio_note_result.group(3), time=None, output_path=f"{self.output_directory}/audio{i}.mp3", tts_components=tts_components, style=audio_note_result.group(2))
    #                     )
    #                 else:
        
    #                     audio_notes.append(
    #                         AudioNote(text=audio_note_result_with_time.group(4), time=audio_note_result_with_time.group(3), output_path=f"{self.output_directory}/audio{i}.mp3", tts_components=tts_components, style=audio_note_result_with_time.group(2))
    #                     )
    #     else:
    #         audio_notes.append(
    #             AudioNote(text=self.audio_notes, time=None,
    #                       output_path=f"{self.output_directory}/audio{0}.mp3",  tts_components=tts_components, style="default")
    #         )

    #     return audio_notes


    # def get_resource_image(self) -> str:
    #     '''Get the resource image of the page
    #     '''
    #     regex = r"]\(([^\)]+)\)"
    #     result = re.search(regex, self.markdown_text)
    #     result = result.group(1) if result else " "
    #     return result


    # def get_resource_video(self):
    #     '''Get the resource video of the page
    #     '''
    #     regex = r"<video.*src=[\"'](.*)[\"']"
    #     result = re.search(regex, self.markdown_text)
    #     result = result.group(1) if result else " "
    #     return result


   

    # ## CHEKC ONLY WEB SOURCES NOW
    # def generate_video(self) -> str: #CHECK CHECK
    #     '''Converts slide image to video using moviepy

    #         Return:
    #             str : generated file path
    #     '''
    #     if ".mp4" in self.markdown_text:
    #         if "```" in self.markdown_text:  # patch
    #             pass
    #         else:
    #             result = self.get_resource_video()
    #             return download_video(result,  f"{self.output_directory}/{self.id}-external.mp4")
    #     else:
    #         #PROCESS
    #         image = self.generate_image()
    #         return create_video(image, f"{self.output_directory}/{self.id}")





