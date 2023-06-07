'''Module with the content and audio notes of the page
'''
import re
import os
from src.entities.settings import Settings
from src.entities.tts_components import TTSComponents
from src.entities.audio_note import AudioNote
from src.lupo.api_lupo import generate_image
from src.lupo.api_lupo import generate_video
from os.path import exists 
from os.path import basename
from moviepy.editor import AudioFileClip
from moviepy.editor import CompositeAudioClip

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

    
    def generate_source(self):
        if ".mp4" in self.markdown_text:
            if "```" in self.markdown_text:  # patch
                pass
            else:
                result = self.get_resource_video()
                return result
        else:
            markdown_text = f"---\n{self.marp_header}\n---\n\n{self.markdown_text}"
            theme_file = self.get_current_theme(self.settings.themes)
            with open(theme_file, 'r', encoding='utf-8') as file:
                theme = file.read()
            image = generate_image(markdown_text, theme)
            return image



    # def generate_video(self, source, audio_notes):
    #     if not "silence.mp3" in audio_notes:
    #         if "mp4" in source:
    #             source_type = "video"
    #         else:
    #             source_type = "image"
    #         complete_audio_note = self.composite_audio_notes(audio_notes)
    #         video = generate_video(source, source_type, complete_audio_note, not self.settings.final)
    #         return video



    # def composite_audio_notes(self, audio_notes):
    #     '''Extract the audio notes from an external video.

    #         Parameters:
    #             audio_notes(list): List of the audio notes for the external video

    #         Return:
    #             src
    #     '''

    #     final_audio_clip = None

    #     for audio_note in audio_notes:
    #         print(audio_note.output_path)
    #         temporal_audio_clip = AudioFileClip(
    #             audio_note.output_path, fps=48000)

    #         if final_audio_clip is None:
    #             if audio_note.time is not None:
    #                 final_audio_clip = temporal_audio_clip
    #                 final_audio_clip = final_audio_clip.set_start(
    #                                         (audio_note.hours, audio_note.minutes, audio_note.seconds))
    #             else:
    #                 final_audio_clip = temporal_audio_clip
    #         else:
    #             if audio_note.time is not None:
    #                 final_audio_clip = CompositeAudioClip([
    #                     final_audio_clip,
    #                     temporal_audio_clip.set_start(
    #                         (audio_note.hours, audio_note.minutes, audio_note.seconds))
    #                 ])
    #             else:
    #                 final_audio_clip = CompositeAudioClip([
    #                     final_audio_clip,
    #                     temporal_audio_clip.set_start(final_audio_clip.duration)
    #                 ])

        
    #     audio = f"{self.settings.course_name}_{self.page_id}.mp3"
    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    #     file_path = os.path.join(current_dir,audio )
    #     final_audio_clip.write_audiofile(file_path, codec='libmp3lame', fps=48000 )
        
    #     file_name = basename(file_path)
    #     #final_audio_clip = upload_file_to_azure_blob_storage("courses", file_path, blob_name=f"{course_name}/assets/{file_name}")
    #     os.remove(file_path)
    #     return final_audio_clip



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
