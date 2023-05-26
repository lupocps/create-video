'''Utils Functions and Variables'''

import os
import sys
import logging
import yaml


HEADERS_LUPO = {'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br'}


ENDPOINT_USER = "https://lupo.ai/api/ProjectRuns"


#ENDPOINT SERVER LUPO, TEMPORAL
ENDPOINT_LUPO = "https://20.55.24.28:50000/api"


RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'


LANGUAGE_TRANSLATION_DICT = {
    'spanish': 'es',
    'english': 'en',
    'italian': 'it',
    'thai': 'th',
    'arabic': 'ar',
    'chinese': 'zh-Hans',
    'german': 'de',
    'french': 'fr',
    'japanese': 'ja',
    'korean': 'ko',
    'portuguese': 'pt',
    'russian': 'ru',
    'swedish': 'sv',
    'romanian': 'ro',
    'irish': 'ga',
    'indonesian': 'id',
    'hungarian': 'hu',
    'filipino': 'fil',
    'croatian': 'hr',
    'dutch': 'nl'
}



def log(message: str, level: str = logging.INFO):
    '''Log a message to the console using the specified logging level.

    Parameters:
        message (str): The message to log.
        level (int): The logging level to use. Default is logging.INFO.
    '''
    logging.basicConfig(
        filename='app.log',
        filemode='w',
        level=logging.INFO,
        format='%(message)s'
    )
    if level.lower() == 'info':
        message = f"{CYAN}INFO - {message}{RESET}"
        logging.info(message)
    elif level.lower() == 'success':
        message = f"{GREEN}SUCCESS - {message}{RESET}"
        logging.info(message)
    elif level.lower() == 'warning':
        message = f"{YELLOW}WARNING - {message}{RESET}"
        logging.warning(message)
    elif level.lower() == 'error':
        message = f"{RED}ERROR - {message}{RESET}"
        logging.error(message)
        github_repo = os.environ["GITHUB_REPOSITORY"]
        send_error_message(message, github_repo)
    elif level.lower() == 'critical':
        message = f"{RED}CRITICAL - {message}{RESET}"
        logging.critical(message)
        github_repo = os.environ["GITHUB_REPOSITORY"]
        send_error_message(message, github_repo)
    else:
        logging.debug(message)


def send_error_message(message, github_repo):
    '''Send error message to user
    
    Parameters:
        message(str): Source message of the error
        github_repo(str): Repo of the user
    '''

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '../utils/message_error.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        error_message = file.read()
        error_message = error_message.replace('[REPO]', github_repo)
        error_message = error_message.replace('[ERROR_MESSAGE]', message)
    print(error_message)
    sys.exit(1)
    


def read_toc(toc):
    '''Read the toc.yml file
    
    Parameters:
        toc(str): The string of the toc file

    Returns:
        (dict): A dictionary of the toc file
    '''
    with open(toc, "r", encoding="utf-8") as file:
        try:
            yaml_dict = yaml.load(file.read(), Loader=yaml.SafeLoader)
            log("YAML file loaded successfully.", "success")

        except yaml.YAMLError as error:
            with open(toc, 'r', encoding="utf-8") as file:
                try:
                    log(f"the first chapter 'name' key missing or there a problem with the indentation in the toc file: {error}", "error")
                except FileNotFoundError:
                    log(f"The file {toc} was not found.", "error")

     
    return yaml_dict

