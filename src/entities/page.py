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
        markdown_source_notes = re.sub(r'<mstts:express-as style="[^"]*">(.*?)<\/mstts:express-as>', r'\1', audio_notes)
        self.source_audio_notes = markdown_source_notes



    def generate_audio_notes(self, tts_components: TTSComponents) -> list:
        '''Converts each audio line to a AudioNote object.

            Return:
                list : AudioNote objects array
        '''
  
        print("enter generate audio ntoes")
        audio_notes = [] 
        if 'https://mlgstorageaccount.blob.core.windows.net/docs/media/silence.mp3' in self.audio_notes:
            return self.audio_notes

        regex_with_time = r'<mstts:express-as style=("([^"]+)")>\(\((\d+(?:,\s*\d+)*)\)\)\s*(.*?)<\/mstts:express-as>'
        regex_no_time = r'<mstts:express-as style=("([^"]+)")>\s*(.*?)<\/mstts:express-as>'
        has_time = re.search(
            r'\(\(', self.audio_notes, re.MULTILINE)  # Has time
        
        if has_time:
            for i, line in enumerate(self.audio_notes.split('\n')):
                if len(line) > 1:
                    audio_note_result_with_time = re.search(regex_with_time, line)
                    if  audio_note_result_with_time is None:
                        audio_note_result = re.search(regex_no_time, line)
                        audio_notes.append(
                            AudioNote(text=audio_note_result.group(3), time=None, tts_components=tts_components, style=audio_note_result.group(2))
                        )
                    else:
        
                        audio_notes.append(
                            AudioNote(text=audio_note_result_with_time.group(4), time=audio_note_result_with_time.group(3), tts_components=tts_components, style=audio_note_result_with_time.group(2))
                        )
        else:
            audio_notes.append(
                AudioNote(text=self.audio_notes, time=None,
                        tts_components=tts_components, style="default")
            )

        return audio_notes
