import argparse
import os

import openai
import pandas as pd

from repository import GitRepo

openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    parser = argparse.ArgumentParser(description='Run Code Explainer on a Git Repo')
    parser.add_argument('--repo_url', required=True, help='URL of the git repository')
    parser.add_argument('--output_file', required=True, help='path of the output json file')
    args = parser.parse_args()

    repo = GitRepo(args.repo_url)
    repo.clone()
    file_paths = repo.list_files()
    explanations = []
    index = 0
    for file_path in file_paths:
        print("-"*100)
        relative_file_path = os.path.relpath(file_path, repo.repo_path)
        print(relative_file_path)
        index += 1
        if index > 10:
            break
        with open(file_path, 'r') as fin:
            data = fin.read()
        if len(data) > 40000:
            print(f"{file_path} has a character size exceeding limit. Skipping ...")
        prompt_text = data + "\n\n# Brief Explanation of what the code above does \n#"
        response = response = openai.Completion.create(
            model="code-davinci-002",
            prompt=prompt_text,
            temperature=0.1,
            max_tokens=512,
            top_p=1.0,
            frequency_penalty=0.3,
            presence_penalty=0.1
        )
        explanation = response.get("choices", [{}])[0].get("text")
        print("-"*100)
        print(explanation)

        explanations.append({'file_path': relative_file_path, 'explanation': explanation})

    df = pd.DataFrame.from_records(explanations)
    df.to_json(args.output_file)


if __name__ == '__main__':
    main()
