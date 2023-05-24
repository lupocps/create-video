'''Lupo Compiler'''

import unicodedata
import json
from os.path import exists
from src.utils import print_log


def validate_yaml_file_details(root_folder:str, yaml_dict:str):
    '''Validate the details of the yaml file
    
    Parameters:
        root_folder(str):
        yaml_file (str):
    
    Return:
        (Settings):
    
    '''
    root_folder = root_folder.replace("\\", "/")

    course_name = yaml_dict['name'] if 'name' in yaml_dict else '' 
    print(course_name)
    course_version = yaml_dict['version'] if 'version' in yaml_dict else '' 
    course_speaker = yaml_dict['speaker'] if 'speaker' in yaml_dict else ''
    trailer_mode = yaml_dict['trailer'] if 'trailer' in yaml_dict else False


    speakers = course_speaker.split(",")
    if len(speakers) > 1:
        speakers = [speaker.strip() for speaker in speakers]
        #TODO: delete duplicates
        if not trailer_mode:
           course_speaker = speakers[0]


    # CHECK DETAILS
    if course_name == '':
        print_log("The yaml file has no 'name' key.", 'warning')
    if course_version == '':
        print_log("The yaml file has no 'version' key.", 'warning')
    if course_speaker == '':
        print_log("The yaml file has no 'speaker' key.", 'warning')
        course_speaker = 'Aria'


    languages_to_translate = yaml_dict['translate'] if 'translate' in yaml_dict else '' 
    
    style_speaker = yaml_dict['style'] if 'style' in yaml_dict else 'default'
    audio_speed = yaml_dict['speed'] if 'speed' in yaml_dict else 1.0
    audio_pitch = yaml_dict['pitch'] if 'pitch' in yaml_dict else 1.0
    
    # Check if file exists
    themes = "" #
    print(f"{root_folder}/.vscode/settings.json") 
    if exists(f"{root_folder}/.vscode/settings.json"):
        with open(f"{root_folder}/.vscode/settings.json", encoding="utf-8") as file:
            try:
                print("exist the theme file")
                data = json.load(file)
                if "markdown.marp.themes" in data:
                    themes = " ".join([f"{root_folder}/{t}" for t in data["markdown.marp.themes"]])
                else:
                    print_log("No 'markdown.marp.themes' attribute found in settings.json", "WARNING")
            except FileNotFoundError:
                print("No exist file")
                print_log("The file was not found.", "ERROR")
    else:       
        print_log("The '.vscode/settings.json' file does not exist. Unable to generate themes.", "WARNING")
    print("themes:", themes)
    # Validate attributes
    course_name = slugify(course_name)
    course_version = slugify(course_version)

    #languages_to_translate = validate_languages(languages_to_translate)

    course_speaker = course_speaker.capitalize()
   # if not has_style_in_lupo(style_speaker, course_speaker):
   #     style_speaker = "default"


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