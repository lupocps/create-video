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
    body = {"text": text, "speaker":speaker, "style": style, "speed": speed, "pitch": pitch}
    print("body", body)
    response = requests.post(ENDPOINT_LUPO+"/audios", HEADERS_LUPO, json=body,timeout=20)
    print("status_code", response.status_code)
    if response.status_code == 200:
        print("audio", audio)
        audio = response.json()
        print("audio", audio)
    else:
        log("Problem with connecting to the API ", "warning")
        audio = "https://mlgstorageaccount.blob.core.windows.net/docs/media/silence.mp3"

    return audio

