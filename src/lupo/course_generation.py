'''This module provides functions for generating videos and courses based on the specified sections.'''

from os.path import basename
from src.utils import log
from src.utils import upload_file_to_azure_blob_storage
from src.entities.settings import Settings


def generate_course(chapters:list, settings:Settings, azure_folder:str, course_data:dict) -> dict:
    '''Generate the Lupo Videos in a dictionary
    
    Parameters:
        chapters(list):
        settings(Settings):
        azure_folder(str):
        course_data(dict):
    
    Return:
        (dict):
    '''

    for chapter in chapters:
        chapter_data = {
            "Name": chapter.name,
            "Sections": []
        }

        for section in chapter.sections:
            video = section.generate_video()
            video_azure_link = upload_file_to_azure_blob_storage("courses", video,
                blob_name=f"{azure_folder}/{chapter.chapter_id}-{chapter.name}/{section.name}-{section.section_id}.mp4")
            if settings.trailer_mode:
                settings.mail.set_video(video_azure_link, chapter.name, f"{section.tts_components.voice_speaker}/{section.name}")
            else:
                settings.mail.set_video(video_azure_link, chapter.name, section.name)

            captions_azure_link = ''
            if settings.generate_captions:
                #captions_azure_link = generate_captions_by_section(
          #          video, chapter, section, settings, azure_folder)
                pass

            section_data = {
                "Name": section.name,
                "Video": video_azure_link,
                "Captions": [caption for caption in captions_azure_link.split("\n") if caption]
            }

            chapter_data["Sections"].append(section_data)

        log(f'Video of chapter {chapter.id} generated.', 'info')

        if settings.generate_transcript:
          #  chapter_data = generate_transcript_by_chapter(
         #       chapter_data, chapter, settings, azure_folder)
            pass
        if settings.generate_slides:
           # chapter_data = generate_slides_by_chapter(
           #     chapter_data, chapter, settings, azure_folder)
            pass
        course_data["Chapters"].append(chapter_data)

    return course_data

