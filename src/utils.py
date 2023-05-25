'''Utils Functions and Variables'''

import os
import sys
import yaml
import logging

HEADERS_LUPO = {'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br'}


ENDPOINT_USER = "https://lupo.ai/api/ProjectRuns"


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

logging.basicConfig(
    filename='app.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define custom log formatter
log_formatter = logging.Formatter('%(asctime)s - %(level)s - %(message)s')
# Set up console logger with custom formatter
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(console_handler)


def log(message: str, level: str = logging.INFO):
    '''Log a message to the console using the specified logging level.

    Parameters:
        message (str): The message to log.
        level (int): The logging level to use. Default is logging.INFO.
    '''
    logger = logging.getLogger()

    if level.lower() == 'info':
        message = f"{CYAN}{message}{RESET}"
        logger.info(message)
    elif level.lower() == 'success':
        message = f"{GREEN}{message}{RESET}"
        logger.info(message)
    elif level.lower() == 'warning':
        message = f"{YELLOW}{message}{RESET}"
        logger.warning(message)
    elif level.lower() == 'error':
        message = f"{RED}{message}{RESET}"
        logger.error(message)
        github_repo = os.environ["GITHUB_REPOSITORY"]
        send_error_message(message, github_repo)
    elif level.lower() == 'critical':
        message = f"{RED}{message}{RESET}"
        logger.critical(message)
        github_repo = os.environ["GITHUB_REPOSITORY"]
        send_error_message(message, github_repo)
    else:
        logger.debug(message)


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
                  #  send_error_message(f"the first chapter 'name' key missing or there a problem with the indentation in the toc file: {error}", github_repo)
                except FileNotFoundError:
                    log(f"The file {toc} was not found.", "error")
                  #  send_error_message(f"The file {toc} was not found.", github_repo)
     
    return yaml_dict

