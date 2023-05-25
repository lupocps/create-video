'''GitHub verification'''

import sys
import requests
from src.utils import ENDPOINT_USER
from src.utils import HEADERS_LUPO
from src.utils import print_log

def user_verification(is_final, github_actor, github_repository, output_string) -> dict:
    '''Verification a GitHub User in Lupo Web
    
    Parameters:
        
    '''
    

    print_log(f"Actor: {github_actor}, Repository: {github_repository}", "INFO")
    output_string += f"Actor: {github_actor}, Repository: {github_repository}\n"
    print("output_string in user verification: ", output_string)
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

    message_error = f'{github_actor} user validation did not complete successfully'
    print_log(message_error, "ERROR")
    sys.exit(1)

    