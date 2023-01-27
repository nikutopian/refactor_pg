import argparse
import os

import pandas as pd

from repository import GitRepo
from openai_utils import OpenAIWrapper

MAX_NUM_FILES = 10

def main():
    parser = argparse.ArgumentParser(description='Run Code Explainer on a Git Repo')
    parser.add_argument('--repo_url', required=True, help='URL of the git repository')
    parser.add_argument('--output_file', required=True, help='path of the output json file')
    args = parser.parse_args()

    repo = GitRepo(args.repo_url)
    repo.clone()
    file_paths = repo.list_files()

    wrapper = OpenAIWrapper()

    explanations = []
    index = 0

    for file_path in file_paths:

        relative_file_path = os.path.relpath(file_path, repo.repo_path)
        index += 1
        if index > MAX_NUM_FILES:
            print("Reached MAX number of files. Exiting ...")
            break

        print("-"*100)
        print(f"Relative File Path: {relative_file_path}")

        with open(file_path, 'r') as fin:
            code_string = fin.read()
        if len(code_string) > 40000:
            print(f"{file_path} has a character size exceeding limit. Skipping ...")

        explanation = wrapper.explain_code(code_string)

        print("-"*100)
        print(explanation)

        explanations.append({'file_path': relative_file_path, 'explanation': explanation})

    df = pd.DataFrame.from_records(explanations)
    df.to_json(args.output_file)


if __name__ == '__main__':
    main()
