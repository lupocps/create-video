'''Module with the content and audio notes of the page
'''
import re
from src.entities.settings import Settings
from src.entities.tts_components import TTSComponents
from src.entities.audio_note import AudioNote

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
       # markdown_source_notes = re.sub(r'<mstts:express-as style="[^"]*">(.*?)<\/mstts:express-as>', r'\1', audio_notes)
       # self.source_audio_notes = markdown_source_notes



    def generate_audio_notes(self, tts_components: TTSComponents) -> list:
        '''Converts each audio line to a AudioNote object.

            Return:
                list : AudioNote objects array
        '''
  
       
        print("enter generate audio notes")
        audio_notes = [] 
        if 'https://mlgstorageaccount.blob.core.windows.net/docs/media/silence.mp3' in self.audio_notes:
            return self.audio_notes

        for audio_dict in self.audio_notes:
            has_time = re.search(
            r'\(\(', audio_dict["text_audio_note"])
            if has_time:
                audio_note_result = re.search(
                    r'(\(\(([\d\., ]*)\)\))?(.*)', audio_dict["text_audio_note"])

                audio_notes.append(
                            AudioNote(text=audio_note_result.group(3), time=audio_note_result.group(2), tts_components=tts_components, style=audio_dict["text_audio_note"])
                        )
            else:
                audio_notes.append(
                            AudioNote(text=audio_dict["text_audio_note"], time=None, tts_components=tts_components, style=audio_dict["text_audio_note"])
                        )

        return audio_notes

