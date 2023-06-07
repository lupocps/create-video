'''Azure Connector'''


import requests

from src.utils import log
from src.utils import ENDPOINT_LUPO
from src.utils import HEADERS_LUPO

def generate_audio(
    text: str,
    speaker: str,
    style: str,
    speed: float,
    pitch: float,
    ) -> str:
    '''Generate Audio using azure Text-To-Speech

    Parameters:
        text (str): #TODO
        speaker (str): #TODO
        style (str): #TODO
        speed (float): #TODO
        pitch (float): #TODO

    Returns:
        str: path of the generated audio file
    '''
    
    if text == "https://mlgstorageaccount.blob.core.windows.net/docs/media/silence.mp3":
        return text
    
    body = {'text': text, 'speaker': speaker, 'style': style, 'speed': speed, 'pitch': pitch}

    response = requests.post(ENDPOINT_LUPO+"/audios", headers=HEADERS_LUPO, json=body,timeout=20)

    if response.status_code == 200:
        audio = response.json()
        audio = audio['audio_url']
        print("audio", audio)
    else:
        log("Problem with connecting to the API ", "warning")
        audio = "https://mlgstorageaccount.blob.core.windows.net/docs/media/silence.mp3"

    return audio


def generate_image(markdown_text, theme):
    body = {'markdown':markdown_text, 'style' : theme}
    response = requests.post(ENDPOINT_LUPO+"/images", headers=HEADERS_LUPO, json=body,timeout=20)

    if response.status_code == 200:
        image = response.json()
        image = image['image_url']
        print("image", image)
    else:
        log("Problem with connecting to the API ", "warning")
        #BLANK or WITH MESSAGE IMAGE?
    return image


def generate_video(source, source_type, audio_notes, draft):
    body = {'source': source, 'source_type': source_type , 'audio': audio_notes, 'draft': draft, 'is_console_application': True}
    print("body", body)
    print("audionotes",audio_notes )
    response = requests.post(ENDPOINT_LUPO+"/videos", headers=HEADERS_LUPO, json=body,timeout=20)
    if response.status_code == 200:
        video = response.json()
        video = video['video_url']
        print("video", video)
    else:
        log("Problem with connecting to the API ", "warning")
        
    return video


def concatenate_videos(videos):
    body = {'video_urls': videos}
    print("body", body)
    response = requests.post(ENDPOINT_LUPO+"/concatenate_videos", headers=HEADERS_LUPO, json=body,timeout=20)
    if response.status_code == 200:
        video_response = response.json()
        time = video_response['time']
        video = video_response['video_url']
        print("video", video)
    else:
        log("Problem with connecting to the API ", "warning")
        
    return video, time