
'''Utils Functions and Variables'''


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

