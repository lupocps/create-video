'''Utils Functions and Variables'''

import os
import sys
import yaml

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


def print_log(message, level='INFO'):
    '''Print in the console info of Lupo
    '''
    color = {
        'PROGRESS': BLUE,
        'WARNING': YELLOW,
        'ERROR': RED,
        'SUCCESS': GREEN,
        'INFO': CYAN
    }.get(level.upper(), '')

    styled_message = f"{color}{message}{RESET}"
    print(styled_message)



def send_error_message(message, github_repo):
    '''Send error message to user
    
    Parameters:
        message(str): Source message of the error
        github_repo(str): Repo of the user
    '''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("current dir", current_dir)
    file_path = os.path.join(current_dir, '../utils/message_error.txt')
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        error_message = file.read()
        error_message = error_message.replace('[REPO]', github_repo)
        error_message = error_message.replace('[MESSAGE]', message)
    print(error_message)
    sys.exit(1)
    


def read_toc(toc, github_repo):
    '''Read the toc.yml file
    
    Parameters:
        toc(str): The string of the toc file

    Returns:
        (dict): A dictionary of the toc file
    '''
    print(toc)
    with open(toc, "r", encoding="utf-8") as file:
        try:
            yaml_dict = yaml.load(file.read(), Loader=yaml.SafeLoader)
            print_log("YAML file loaded successfully.", "SUCCESS")
        except yaml.YAMLError as error:
            with open(toc, 'r', encoding="utf-8") as file:
                try:
                    send_error_message(f"the first chapter 'name' key missing or there a problem with the indentation in the toc file: {error}", github_repo)
                except FileNotFoundError:
                    send_error_message(f"The file {toc} was not found.", github_repo)
     
    return yaml_dict

