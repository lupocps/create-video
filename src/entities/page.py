'''Module with the content and audio notes of the page
'''
import re
from src.entities.settings import Settings


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
        print("marp_header", self.marp_header)
        self.markdown_text = markdown_text
        print("markdown_text", self.markdown_text)
        self.audio_notes = audio_notes
        print("audio_notes", self.audio_notes)
        self.settings = settings
        self.source_md = "" ## check
        markdown_source_notes = re.sub(r'<mstts:express-as style="[^"]*">(.*?)<\/mstts:express-as>', r'\1', audio_notes)
        self.source_audio_notes = markdown_source_notes
        print("source_audio_notes: ", self.source_audio_notes)


