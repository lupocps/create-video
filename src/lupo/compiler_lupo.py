'''Lupo Compiler'''

import unicodedata
import json
import re
from os.path import exists
from os.path import normpath
from os.path import join
from os.path import basename
import requests
from src.utils import log
from src.utils import LANGUAGE_TRANSLATION_DICT
from src.utils import ENDPOINT_LUPO
from src.utils import HEADERS_LUPO
from src.utils import SPEED_CONSTANTS
from src.utils import PITCH_CONSTANTS
from src.utils import MARP_DIRECTIVES
from src.utils import upload_file_to_azure_blob_storage

from src.entities.tts_components import TTSComponents
from src.entities.settings import Settings


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
                    themes = " ".join(t for t in data["markdown.marp.themes"])
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


    tts_components = TTSComponents(
            course_speaker,  rectify_speed(audio_speed), rectify_pitch(audio_pitch), style_speaker)


    return Settings(yaml_dict, course_name, course_version, tts_components, languages_to_translate,themes, trailer_mode)


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
        voices_speaker = voices_speaker['voices_with_styles']
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


def rectify_speed(speed: str) -> str:
    '''Check if exist the rate for the text-to-speech

    Parameters:
        speed (str): Indicate the speaking rate of the text

    Return:
        str : The speaking rate (default=default)
    '''
    if isinstance(speed, float) or speed == 2:
        if speed > 2 or speed < 0.5:
            log('The speed range must be between 0.5 and 2', 'warning')
        return str(speed)
    if speed in SPEED_CONSTANTS:
        return str(SPEED_CONSTANTS[speed])
    log('The speed constant does not exist', 'warning')
    return 'default'



def rectify_pitch(pitch: str) -> str:
    '''Check if exist the pitch for the text-to-speech

    Parameters:
        speed (str): Indicate the baseline pitch for the text

    Return:
        str : The speaking rate (default=default)
    '''

    if isinstance(pitch, str):
        if not pitch in PITCH_CONSTANTS:
            log('The pitch constant does not exist', 'warning')
            pitch = PITCH_CONSTANTS['default']
        else:
            pitch = PITCH_CONSTANTS[pitch]

    result = int((pitch - 1) * 100)
    if result == 0:
        return "default"
    if pitch < 0.5 or pitch > 1.5:
        log('The pitch range must be between 0.5 and 1.5', 'warning')
    return f"+{result}.00%" if result > 0 else f"{result}.00%"



def is_path_creatable(pathname: str) -> bool:
    '''Check if the path is creatable.

        Parameters:
            pathname (str): Path to check

        Return:
            bool: True if the string has sufficient permissions to create the path
    '''
    if bool(re.match('^[a-zA-Z0-9_ ]*$', pathname)) is True:
        return True
    return False


def fix_relative_paths(markdown_text: str, markdown_absolute_path: str, course_name):
    '''Change each resource path (image, video, backgroundImage) to their respective azure urls

    Parameters:
        markdown_text (str): Content of the markdown of the section
        markdown_absolute_path (str): path of the markdown
    '''
    regex_list = [
        r"!\[(.*)\]\((?!(http|https)://)(.*)\)",
        r"'!\[(.*)\]\((?!(http|https)://)(.*)\)'", #WITH ' for footer in content
        r"(backgroundImage):\s*url\((?!(http|https)://)(.*)\)",
        r"<video(.*)src=[\"'](?!(http|https)://)(.*)[\"'](.*)>"
    ] 

    for regex in regex_list:
        matches = re.finditer(regex, markdown_text, re.MULTILINE)
        for match in matches:
          #  print("The match is:", match.group(3))
            filename = match.group(3)
            if "../" in filename: # If not are in the same folder as the md
              #  print("the file name in the if is", filename)
                filename_temp = filename.replace("../", "")
                local_file = filename_temp
              #  print("the local file in the if is ", local_file)
            else:
                local_file = normpath(join(markdown_absolute_path, filename)).replace("\\", "/")
              #  print("the local file in the else is", filename)

            if exists(local_file):
              #  print("exist the file")
                file_name = basename(local_file)
              #  print("base name", file_name)
               # url = upload_file_to_azure_blob_storage("courses",
               #     local_file,
              #      blob_name=f"{course_name}/assets/{file_name}")
               # print("url", url)
               # url = "a"
              #  markdown_text = markdown_text.replace(filename, url)
                #print("markdown_text?DDDD", markdown_text)
            else:
             #   print("the file $ does not exist", local_file)
                log(f"The media path does not exist {local_file}", "warning")
    if "<video" in markdown_text:
        if "```" in markdown_text:  # patch again
            pass
        else:
            markdown_text = markdown_text.replace(
                "<video", "<video width=\"1280\" height=\"720\" ")

    return markdown_text



def validate_header(markdown_header:str, themes:str, section_name:str) -> list:
    '''Validate the header of the markdown
    
    Parameters:
        markdown_header(str):
        themes (str):
        mail (Email):
        md_file (str):

    Return:
        (str):
        (str):

    '''
    directives = markdown_header.split("\n")
    directives = list(filter(lambda item: item != '', directives)) # Remove '' elements
    header_validated = "---\n"
    current_theme = ""
    if not directives[0].startswith("marp: true"):
        log(f"The marp directive in the section {section_name} is not found", "error")
    else:
        print("marp check")
        header_validated += directives[0] + "\n"
    for directive in directives[1:]:
        if directive.startswith("theme: "):
            print("check theme")
            current_theme = validate_theme_file(directive, themes, section_name)
            header_validated += directive + "\n"
        elif directive.startswith(MARP_DIRECTIVES):
            header_validated += directive + "\n" # CHECK THE FORMAT OF THE MARP DIRECTIVE?
        else:
            log(f"The format of the header in the file {section_name} not is correct", "error")

    header_validated += "---" + "\n\n"
    return header_validated, current_theme



def validate_theme_file(current_theme:str, themes:str, section_name:str) -> str:
    '''Validate if exists a theme file in a markdown file
    
    Parameters:
        current_theme (str):
        themes (str):
        md_file (str):
    
    Return:
        (str):
    '''
    substring = "theme:"
    current_theme = current_theme.split(substring, 1)[-1].strip()
    current_theme_file = f"{current_theme}.css"
    themes = themes.split(" ")
    for theme in themes:
        theme_name = basename(theme)
        if current_theme_file == theme_name:
            if exists(theme):
                return theme
            log(f"The theme {theme} does not exists", "warning")
            return ""
    
    log(f"The theme of the file {section_name} does not exist in the local themes", "warning")
    return ""


def extract_content_audio_compiler(markdown_page: str, page_id, section_file_name: str):
    '''Extract the content and audio for each page
    
    Parameters:
        markdown_page (str): markdown page
        page_id (str): id of the page
        section_file_name (str): section file name

    Return:
        list():

    '''
    if markdown_page == "":
        log(f"The slide number {page_id} of the file {section_file_name} is empty", "warning")

    result = re.search(r"((.|\n)*)<!--\s*((.|\n)*)\s*-->", markdown_page)
  
    if result is None: # NO audio TAG
        log(f"The are not a narration tag in {section_file_name} in the slide number {page_id}", "warning")
        return markdown_page, "../utils/silence.mp3"
    audio_note = result.group(3).strip()
    markdown_text = result.group(1).strip()
    if audio_note == '': # AUDIO TAG EMPTY
        log(f"The are a narration empty in {section_file_name} in the slide number {page_id}", "warning")
        return markdown_text, "../utils/silence.mp3"
    if audio_note.startswith(MARP_DIRECTIVES): ## AUDIOTAG WITH MARP DIRECTIVES
        log(f"The narration cannot have marp directive in {section_file_name} in the slide number {page_id}", "warning")
        return markdown_page, "../utils/silence.mp3"
    return markdown_text, audio_note



def validate_md_content(markdown_content:str, page_id:int, section_file_name:str, current_theme_file:str) -> str:
    '''Validate the content of a markdown file 
    
    Parameters:
        markdown_content (str):
        page_id (int):
        section_file_name (str):
        current_theme_file (str):
    
    Return:
        (str):
    '''
    if markdown_content == "": #Content empty
        log(f"The content of a slide number {page_id} of the file {section_file_name} is empty", "warning")
        markdown_content = "\n"
    else:
        if current_theme_file != "":
            theme_regex = r'<!--\s*[_]?class:\s*(\w+)\s*-->'
            matches = re.findall(theme_regex, markdown_content)
            for match in matches:
                with open(current_theme_file, "r", encoding='utf-8') as file:
                    content = file.read()
                    if not match in content:
                        log(f"The class {match} is not in {current_theme_file} file", "warning")
        else:
            log("The MD does not using a theme", "warning")
    return markdown_content + "\n\n"

