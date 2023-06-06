'''Module with the content and audio notes of the page
'''
import re
from src.entities.settings import Settings
from src.entities.tts_components import TTSComponents
from src.entities.audio_note import AudioNote
from src.lupo.api_lupo import generate_image
from os.path import exists 
from os.path import basename 

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
        print("header page",  self.marp_header)
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
                            AudioNote(text=audio_note_result.group(3), time=audio_note_result.group(2), tts_components=tts_components, style=audio_dict["style"])
                        )
            else:
                audio_notes.append(
                            AudioNote(text=audio_dict["text_audio_note"], time=None, tts_components=tts_components, style=audio_dict["style"])
                        )

        return audio_notes

    
    def generate_image(self):
        if ".mp4" in self.markdown_text:
            if "```" in self.markdown_text:  # patch
                pass
            else:
                result = self.get_resource_video()
                return result
        else:
            markdown_text = f"---\n{self.marp_header}\n---\n\n{self.markdown_text}"
            theme_file = self.get_current_theme(self.settings.themes)
            print("markdown_text", markdown_text)
            with open(theme_file, 'r', encoding='utf-8') as file:
                theme = file.read()
            image = generate_image(markdown_text, theme)
            return image


    def get_resource_video(self):
        '''Get the resource video of the page
        '''
        regex = r"<video.*src=[\"'](.*)[\"']"
        result = re.search(regex, self.markdown_text)
        result = result.group(1) if result else " "
        return result


    def get_current_theme(self, themes):
        '''Get the file of the theme
        '''
        directives = self.marp_header.split("\n")
        directives = list(filter(lambda item: item != '', directives))
        for directive in directives[1:]: #0 is marp: true
            if directive.startswith("theme: "):
                substring = "theme:"
                current_theme = directive.split(substring, 1)[-1].strip()
                current_theme_file = f"{current_theme}.css"
                for theme in themes.split(' '):
                    theme_name = basename(theme)
                    if current_theme_file == theme_name:
                        if exists(theme):
                            
                            return theme
            return ''
