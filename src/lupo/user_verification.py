'''GitHub verification'''

from os import environ
import requests
from src.utils import ENDPOINT_USER
from src.utils import HEADERS_LUPO
from src.utils import log


def user_verification(is_final) -> dict:
    '''Verification a GitHub User in Lupo Web
    
    Parameters:
        
    '''
    github_actor = environ["GITHUB_ACTOR"]
    github_repository = environ["GITHUB_REPOSITORY"]

    log(f"Actor: {github_actor}, Repository: {github_repository}", "info")
    github_repo = f"https://github.com/{github_repository}"

    if is_final:
        output_quality = "final"
    else:
        output_quality = "draft"

    body = {
        'GithubUsername': github_actor,
        'GithubRepo' : github_repo,
        'OutputType' : output_quality
    }


    response = requests.post(ENDPOINT_USER, headers=HEADERS_LUPO, json=body, timeout=20)

    if response.status_code == 200:
        identification = response.json()
        params_for_db = {
            "ProjectBuildId" : identification["projectBuildId"],
            "ProjectBuildPassword" : identification["projectBuildPassword"]
        }
        return params_for_db

    #TODO: More specific message
    message_error = f'{github_actor} user validation did not complete successfully'
    log(message_error, "error")

    