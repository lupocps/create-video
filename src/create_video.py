''' Create Videos '''

import argparse

parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('--author', type=str, required=True)
parser.add_argument('--repo', type=str, required=True)

# Parse the argument
args = parser.parse_args()

print(args.author)
print(args.repo)
