'''Lupo Compiler'''

import unicodedata
import json
import re
from os.path import exists
import requests
from src.utils import log
from src.utils import LANGUAGE_TRANSLATION_DICT
from src.utils import ENDPOINT_LUPO
from src.utils import HEADERS_LUPO


def validate_yaml_file_details(yaml_dict:str):
    '''Validate the details of the yaml file
    
    Parameters:
        root_folder(str):
        yaml_file (str):
    
    Return:
        (Settings):
    
    '''
    #root_folder = root_folder.replace("\\", "/")

    course_name = yaml_dict['name'] if 'name' in yaml_dict else '' 
    course_version = yaml_dict['version'] if 'version' in yaml_dict else '' 
    course_speaker = yaml_dict['speaker'] if 'speaker' in yaml_dict else ''
    trailer_mode = yaml_dict['trailer'] if 'trailer' in yaml_dict else False

    #TODO:
    speakers = course_speaker.split(",")
    if len(speakers) > 1:
        speakers = [speaker.strip() for speaker in speakers]
        #TODO: delete duplicates
        if not trailer_mode:
           course_speaker = speakers[0]


    # CHECK DETAILS
    if course_name == '':
        log("The yaml file has no 'name' key.", 'warning')
    if course_version == '':
        log("The yaml file has no 'version' key.", 'warning')
    if course_speaker == '':
        log("The yaml file has no 'speaker' key.", 'warning')
        course_speaker = 'Aria'


    languages_to_translate = yaml_dict['translate'] if 'translate' in yaml_dict else '' 
    
    style_speaker = yaml_dict['style'] if 'style' in yaml_dict else 'default'
    audio_speed = yaml_dict['speed'] if 'speed' in yaml_dict else 1.0
    audio_pitch = yaml_dict['pitch'] if 'pitch' in yaml_dict else 1.0
    
    # Check if file exists
    themes = "" #
 
    if exists("./.vscode/settings.json"):
        with open("./.vscode/settings.json", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if "markdown.marp.themes" in data:
                    themes = " ".join([t for t in data["markdown.marp.themes"]])
                else:
                    log("No 'markdown.marp.themes' attribute found in settings.json", 'warning')
            except FileNotFoundError:
                log("The file was not found.", 'error')
    else:       
        log("The '.vscode/settings.json' file does not exist. Unable to generate themes.", 'warning')


    # Validate attributes
    # SPEAKER AFTER CHECK MD FILE
    course_name = slugify(course_name)
    course_version = slugify(course_version)

    languages_to_translate = validate_languages(languages_to_translate)

    course_speaker = course_speaker.capitalize()
    if not has_style_in_lupo(style_speaker, course_speaker):
        style_speaker = "default"


    #tts_components = TTSComponents(
    #        course_speaker,  rectify_speed(audio_speed), rectify_pitch(audio_pitch), style_speaker)


    #return Settings(root_folder, yaml_dict, course_name, course_version, tts_components,languages_to_translate,mail,themes, trailer_mode)


def slugify(value: str, allow_unicode=False) -> str:
    '''Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumeric,
    underscores, or hyphens. Convert to lowercase. Also, strip leading and
    trailing whitespace, dashes, and underscores.

    Parameters:
        value (str): String to convert
        allow_unicode (bool): If true, do not convert to ASCII

    Return:
        str: The string converted
    '''
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '_', value).strip('-_')


def validate_languages(languages_to_translate:list) -> list:
    '''Validate the languages of translate

    Parameters:
        languages_to_translate(list):

    Return:
        (list):
    '''
    if languages_to_translate != '':
        languages_to_translate_temp = []
        for language in languages_to_translate.split(","):
            language = language.strip().lower()
            if language in LANGUAGE_TRANSLATION_DICT:
                languages_to_translate_temp.append(LANGUAGE_TRANSLATION_DICT[language])
                language = LANGUAGE_TRANSLATION_DICT[language]
            elif language == 'zh-hans':
                languages_to_translate_temp.append('zh-Hans')
                language = 'zh-Hans' 
            elif language in LANGUAGE_TRANSLATION_DICT.values():
                languages_to_translate_temp.append(language)
            else:
                log(f"The {language} language for translation does not exist.", "warning")

        languages_to_translate = languages_to_translate_temp
        log("Validate all languages finished", "success")
        return languages_to_translate

    return ""


def has_style_in_lupo(style: str, voice_speaker: str) -> bool:
    '''Check if a specific style is available for a given voice speaker.

    Args:
        style (str): The name of the style to check.
        voice_speaker (str): The name of the voice speaker to check.

    Returns:
        bool: True if the style is available for the given voice speaker, False otherwise.
    '''
    if style == "default": # For speakers without styling
        return False
    
    response = requests.get(ENDPOINT_LUPO+"/styles", HEADERS_LUPO, timeout=20)
    if response.status_code == 200:
        voices_speaker = response.json()
        voices_speaker = voices_speaker[0]
        print(voices_speaker)
    else:
        log("Problem with connecting to the API ", "warning")
    if not voice_speaker in voices_speaker:
        log(f"The voice speaker {voice_speaker} has no styles", "warning")
        return False
    if not style.lower() in voices_speaker[voice_speaker]:
        log(f"The voice speaker does not have the {style} style", "warning")
        return False
    return True



# Need a list (example) with the available speakers for not to put non-existent speakers
def rectify_voice_speaker(voice_speaker: str) -> str:
    '''Add the speaker name in the correct format for Azure.

        Parameters:
            voice_speaker (str): Voice speaker of the course

        Return:
            str: Voice speaker with the correct format
    '''
    response = requests.get(ENDPOINT_LUPO+"/speakers", HEADERS_LUPO, timeout=20)
    if response.status_code == 200:
        speakers_lupo = response.json()
    else:
        log("Problem with connecting to the API ", "warning")
    for language, speakers in speakers_lupo.items():
        if voice_speaker in speakers:
            return f"{language}-{voice_speaker}Neural"

    log('The voice speaker does not exist', 'warning')
    # TODO: default speaker for each language
    return "en-US-AriaNeural"
