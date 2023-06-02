'''Utils Functions and Variables'''

import os
import sys
import logging
import yaml
#from azure.storage.blob import BlobServiceClient

HEADERS_LUPO = {'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br'}


ENDPOINT_USER = "https://lupo.ai/api/ProjectRuns"


#ENDPOINT SERVER LUPO, TEMPORAL
ENDPOINT_LUPO = "http://172.171.248.83:5000/api"


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


SPEED_CONSTANTS = {
    "x-slow": 0.5,
    "slow": 0.75,
    "default": 1,
    "fast": 1.5,
    "x-fast": 2
}

PITCH_CONSTANTS = {
    "x-low": 0.5,
    "low": 0.75,
    "default": 1,
    "high": 1.25,
    "x-high": 1.5
}


MARP_DIRECTIVES = (
    "paginate:", "header:", "footer:", "class:", "backgroundColor:",
    "backgroundImage:", "backgroundPosition:", "backgroundRepeat:",
    "backgroundSize:", "color:",
    "_paginate:", "_header:", "_footer:", "_class:", "_backgroundColor:",
    "_backgroundImage:", "_backgroundPosition:", "_backgroundRepeat:",
    "_backgroundSize:", "_color:"
)


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


def upload_file_to_azure_blob_storage(
        container_name,
        file_path,
        expiry=7,
        blob_name=None):
    '''Upload a file to Azure Blob Storage and return the URL of the uploaded file.

    Parameters:
        connection_string (str): The connection string to the Azure Blob Storage account.
        container_name (str): The name of the container to upload the file to.
        file_path (str): The local path of the file to upload.
        blob_name (str): The name to give the blob.

    Returns:
        str: The URL of the uploaded file.
    '''
    connection_string = os.environ["LUPO_CORE_AZURE_STORAGE_CONNECTION_STRING"]
    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Use the local file name as the blob name if it's not provided
    if blob_name is None:
        blob_name = os.path.basename(file_path)

    # Upload the file to Azure Blob Storage
    with open(file_path, 'rb') as data:
        blob_client = container_client.upload_blob(
            name=blob_name, data=data, overwrite=True)

    # Set the blob to be deleted in 7 days
    # blob_properties = blob_client.get_blob_properties()
    blob_client.set_blob_metadata(metadata={'delete_after_days': f'{expiry}'})

    # Return the URL of the uploaded file
    return blob_client.url


