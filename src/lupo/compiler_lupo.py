'''Lupo Compiler'''

import unicodedata
import json
import re
import os
from os.path import exists
from os.path import normpath
from os.path import join
from os.path import basename
from os.path import getsize
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


def validate_yaml_file_details(yaml_dict: str):
    '''Validate the details of the yaml file

    Parameters:
        root_folder(str):
        yaml_file (str):

    Return:
        (Settings):

    '''
    # root_folder = root_folder.replace("\\", "/")

    course_name = yaml_dict['name'] if 'name' in yaml_dict else ''
    course_version = yaml_dict['version'] if 'version' in yaml_dict else ''
    course_speaker = yaml_dict['speaker'] if 'speaker' in yaml_dict else ''
    course_captions = yaml_dict['captions'] if 'captions' in yaml_dict else False
    trailer_mode = yaml_dict['trailer'] if 'trailer' in yaml_dict else False

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
    themes = ""

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
    course_name = slugify(course_name)
    course_version = slugify(course_version)

    if course_captions:
        languages_to_translate = validate_languages(languages_to_translate)

    if trailer_mode:
        tts_components = []
        speakers = course_speaker.split(",")
        speakers = list(set(speakers)) # delete duplicates
        for speaker in speakers:
            course_speaker = speaker.strip().capitalize()
            if not has_style_in_lupo(style_speaker, course_speaker):
                style_speaker = "default"
            tts_components.append(TTSComponents(
                                        course_speaker, 
                                        rectify_speed(audio_speed), 
                                        rectify_pitch(audio_pitch), 
                                        style_speaker))
    else:
        if course_speaker == '':
            log("The yaml file has no 'speaker' key.", 'warning')
            course_speaker = 'Aria'
        else:
            course_speaker = course_speaker.capitalize()
    if not has_style_in_lupo(style_speaker, course_speaker):
        style_speaker = "default"

    tts_components = TTSComponents(
        course_speaker,  rectify_speed(audio_speed), rectify_pitch(audio_pitch), style_speaker)

    return Settings(yaml_dict, course_name, course_version, tts_components, languages_to_translate, themes, trailer_mode)


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


def validate_languages(languages_to_translate: list) -> list:
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
                languages_to_translate_temp.append(
                    LANGUAGE_TRANSLATION_DICT[language])
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
    if style == "default":  # For speakers without styling
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
    response = requests.get(ENDPOINT_LUPO+"/speakers",
                            HEADERS_LUPO, timeout=20)
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
        # WITH ' for footer in content
        r"'!\[(.*)\]\((?!(http|https)://)(.*)\)'",
        r"(backgroundImage):\s*url\((?!(http|https)://)(.*)\)",
        r"<video(.*)src=[\"'](?!(http|https)://)(.*)[\"'](.*)>",
        r'<img[^>]*src=(?!(?:http|https):)["\']?(.*?)["\']?(?:\s|>)' #image HTML
    ]

    for regex in regex_list:
        matches = re.finditer(regex, markdown_text, re.MULTILINE)
        for match in matches:
            if '<img[^>]*src=' in regex:
                 filename = match.group(1)
            else:
                filename = match.group(3)
          #  print("The match is:", match.group(3))
            if "../" in filename:  # If not are in the same folder as the md
              #  print("the file name in the if is", filename)
                filename_temp = filename.replace("../", "")
                local_file = filename_temp
              #  print("the local file in the if is ", local_file)
            else:
                local_file = normpath(
                    join(markdown_absolute_path, filename)).replace("\\", "/")
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
                # print("markdown_text?DDDD", markdown_text)
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


def validate_header(markdown_header: str, themes: str, section_name: str) -> list:
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
    # Remove '' elements
    directives = list(filter(lambda item: item != '', directives))
    header_validated = "---\n"
    current_theme = ""
    if not directives[0].startswith("marp: true"):
        log(
            f"The marp directive in the section {section_name} is not found", "error")
    else:
        header_validated += directives[0] + "\n"
    for directive in directives[1:]:
        if directive.startswith("theme: "):
            current_theme = validate_theme_file(
                directive, themes, section_name)
            header_validated += directive + "\n"
        elif directive.startswith(MARP_DIRECTIVES):
            header_validated += directive + "\n"  # CHECK THE FORMAT OF THE MARP DIRECTIVE?
        else:
            log(
                f"The format of the header in the file {section_name} not is correct", "error")

    header_validated += "---" + "\n\n"
    return header_validated, current_theme


def validate_theme_file(current_theme: str, themes: str, section_name: str) -> str:
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

    if result is None:  # NO audio TAG
        log(
            f"The are not a narration tag in {section_file_name} in the slide number {page_id}. Silence was added as narration", "warning")
        return markdown_page, "../../utils/silence.mp3"
    audio_note = result.group(3).strip()
    markdown_text = result.group(1).strip()
    if audio_note == '':  # AUDIO TAG EMPTY
        log(f"The are a narration empty in {section_file_name} in the slide number {page_id}. Silence was added as narration", "warning")
        return markdown_text, "../../utils/silence.mp3" #CHANGE
    if audio_note.startswith(MARP_DIRECTIVES):  # AUDIOTAG WITH MARP DIRECTIVES
        log(
            f"The narration in {section_file_name}, slide number {page_id}, should not include a marp directive, or it is recommended to always have narration instead. Silence was added as narration", "warning")
        return markdown_page, "../../utils/silence.mp3"
    return markdown_text, audio_note


def validate_md_content(markdown_content: str, page_id: int, section_file_name: str, current_theme_file: str) -> str:
    '''Validate the content of a markdown file 

    Parameters:
        markdown_content (str):
        page_id (int):
        section_file_name (str):
        current_theme_file (str):

    Return:
        (str):
    '''
    if markdown_content == "":  # Content empty
        # PUT MESSAGE IN THE CONTENT?
        log(
            f"The content of a slide number {page_id} of the file {section_file_name} is empty", "warning")
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
    return markdown_content


def validate_narration(tts_components: TTSComponents, audio_note: str, page_id: int, section_file_name: str) -> str:
    '''Validate the narration of a markdown file

    Parameters:
        tts_components (TTSComponents): 
        audio_note (str): The text of the narration in the markdown file
        root_folder (str): The root folder of the markdown file

    Return:
        (str):
    '''
    regex_style = r'\[\[(.*)\]\]\s*(.*)'
    regex_text = r'^(?!\[\[).+$'

    audio_note = replace_characters(audio_note)
    audio_note = validate_phonemes(audio_note)
    has_time = re.search(
        r'^\(\(', audio_note, re.MULTILINE)  # Has time

    text_audio_notes = ""
    if has_time:
        for i, line in enumerate(audio_note.split('\n')):
            if len(line) > 1:  # avoid empty lines
                audio_note_result = re.search(
                    r'(\(\(([\d\., ]*)\)\)\s)*(.*)', line)
                has_style_in_audio_note = re.search(
                    regex_style, audio_note_result.group(3))  # style

                validate_time(audio_note_result.group(1),
                              page_id, section_file_name)

                if has_style_in_audio_note:
                    time_with_style = has_style_in_audio_note.group(1).strip()
                    text_line = f"[[{time_with_style}]] {audio_note_result.group(1)} {has_style_in_audio_note.group(2)}"

                    if has_style_in_lupo(has_style_in_audio_note.group(  # CHECK
                            1), tts_components.voice_speaker):  # exist style
                        text_audio_notes_line = re.sub(
                            regex_style, '<mstts:express-as style="\\g<1>">\\g<2></mstts:express-as>', text_line)
                    else:
                        if has_style_in_lupo(tts_components.course_style, tts_components.voice_speaker):
                            text_audio_notes_line = re.sub(
                                regex_style, f'<mstts:express-as style="{tts_components.course_style}">\\g<2></mstts:express-as>', text_line, flags=re.M)

                        else:
                            text_audio_notes_line = re.sub(
                                regex_style, '<mstts:express-as style="default">\\g<2></mstts:express-as>', text_line, flags=re.M)
                else:
                    if has_style_in_lupo(tts_components.course_style, tts_components.voice_speaker):
                        text_audio_notes_line = re.sub(
                            regex_text, f'<mstts:express-as style="{tts_components.course_style}">\\g<0></mstts:express-as>', line, flags=re.M)

                    else:
                        text_audio_notes_line = re.sub(
                            regex_text, '<mstts:express-as style="default">\\g<0></mstts:express-as>', line, flags=re.M)

                text_audio_notes += text_audio_notes_line + "\n"
    else:
        if has_style_in_lupo(tts_components.course_style, tts_components.voice_speaker):
            text_audio_notes = re.sub(
                regex_text, f'<mstts:express-as style="{tts_components.course_style}">\\g<0></mstts:express-as>', audio_note, flags=re.M)

            text_audio_notes = re.sub(
                regex_style, '<mstts:express-as style="\\g<1>">\\g<2></mstts:express-as>',  text_audio_notes)

        else:
            # HOW CHECK IF ARE SOME  STYLES THAT NOT EXIST ###########
            text_audio_notes = re.sub(
                regex_text, '<mstts:express-as style="default">\\g<0></mstts:express-as>', audio_note, flags=re.M)
            text_audio_notes = re.sub(
                regex_style, '<mstts:express-as style="\\g<1>">\\g<2></mstts:express-as>',  text_audio_notes)
    return text_audio_notes


def replace_characters(audio_notes: str) -> str:
    '''Replace invalid characters in the audio narration.

    Parameters:
        audio_notes (str): The audio narration text to process.

    Return:
        (str): The output text with invalid characters replaced.
    '''
    invalid_dict = {}
    
    root_dir = os.path.abspath(os.sep)
    characters_file = join(root_dir, "replace.txt")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    characters_file = os.path.join(current_dir, "../../replace.txt")

    if exists(characters_file) and getsize(characters_file) > 0:
        # reusing function to fill the dictionary
        invalid_dict = phonemes_dict(characters_file)
        audio_notes = replace(audio_notes, invalid_dict)
        return audio_notes
    else:
        log("The file replace.txt not find or does not have anything in the root folder", "warning")
       # ask  return ""


def replace(input_text: str, word_replace_dict: dict) -> str:
    '''Replace words in the input text with their corresponding word.

    Parameters:
        input_text (str): The input text to process.
        word_replace_dict (dict): A dictionary mapping words to their corresponding invalid characters.

    Return:
        (str): The output text with words replaced.
    '''

    # Generate the regular expression pattern to match word-phoneme pairs
    pattern = re.compile(r"(?<!\w)(" + "|".join(re.escape(word)
                         for word in word_replace_dict.keys()) + r")(?!\w)", re.IGNORECASE)

    # Replace the words in the input text
    output_text = pattern.sub(
        lambda match: word_replace_dict[match.group(1).lower()], input_text)

    return output_text


def validate_phonemes(audio_notes: str, ) -> str:
    '''Validate if the narration contains phonemes and replace them.

    Parameters:
        audio_notes (str): The audio narration text to process.
        root_folder (str): The root folder where the phoneme files are located.

    Return:
        (str): The output text with phonemes replaced.
    '''
    phoneme_dict = {}
    phoneme_known_dict = {}
    phonemes_file = "./phonemes.txt"
    if exists(phonemes_file) and getsize(phonemes_file) > 0:
        phoneme_dict = phonemes_dict(phonemes_file)
        audio_notes = phonemes(audio_notes, phoneme_dict)
    else:
        log("The file phonemes.txt not find or does not have anything in the root folder", "warning")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    phonemes_known_file = os.path.join(current_dir, "../../phonemes-known.txt")
    if exists(phonemes_known_file) and getsize(phonemes_known_file) > 0:
        phoneme_known_dict = phonemes_dict(phonemes_known_file)
        # Remove any duplicates between the two dictionaries
        if phoneme_dict:  # DOES NOT WORK IF THE phonemes file does not exists
            for word in phoneme_dict:
                if word in phoneme_known_dict:
                    del phoneme_known_dict[word]

        audio_notes = phonemes(audio_notes, phoneme_known_dict)
    return audio_notes


def phonemes_dict(phonemes_file: str) -> dict:
    '''Load word-phoneme pairs from a phonemes file into a dictionary.

    Parameters:
        phonemes_file (str): The path to the file containing word-phoneme pairs.

    Return:
        (dict): A dictionary mapping words to their corresponding phonetic transcriptions.
    '''

    word_phoneme_dict = {}
    with open(phonemes_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            # Skip empty lines and lines without an equal sign
            if not line or "=" not in line:
                continue
            word, phonemes = line.strip().split("=")
            phonemes = phonemes.strip()
            # Skip lines where the phonetic transcription is empty
            if not phonemes:
                continue
            word_phoneme_dict[word.lower()] = phonemes
    return word_phoneme_dict


def phonemes(input_text: str, word_phoneme_dict: dict) -> str:
    '''Replace words in the input text with their corresponding phonetic transcriptions.

    Parameters:
        input_text (str): The input text to process.
        word_phoneme_dict (dict): A dictionary mapping words to their corresponding phonetic transcriptions.

    Return:
        (str): The output text with words replaced by Azure TTS SSML tags containing the phonetic transcriptions.
    '''

    # Generate the regular expression pattern to match word-phoneme pairs
    pattern = re.compile(r"\b(" + "|".join(re.escape(word)
                         for word in word_phoneme_dict.keys()) + r")\b", re.IGNORECASE)

    # Replace word-phoneme pairs with Azure TTS SSML tags while preserving casing
    output_text = pattern.sub(
        lambda match: f'<phoneme alphabet="ipa" ph="{word_phoneme_dict.get(match.group(0).lower(), match.group(0))}"></phoneme>',
        input_text
    )
    return output_text


def validate_time(time: str, page_id: int, section_file_name: str):
    '''Validate if the time of the audio is a digit

    Parameters:
        time (str): The time of the audio
    '''
    if time is None:
        return False
    pattern = r"\(\((\d+(?:,\s*\d+)*)\)\)"
    matches = re.findall(pattern, time)
    if matches:
        for match in matches:
            number_list = match.split(",")
            for number in number_list:
                stripped_number = number.strip()
                if not stripped_number.isdigit():
                    log(
                        f"The format time in the slide {page_id} of the section {section_file_name} is not valid", "warning")
                    return False

    return True
