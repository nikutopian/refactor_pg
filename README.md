# Repository for Refactor Project

## Installation
```
pip install -r requirements.txt
```

## Description
Simple code to download a git repository locally, reading all the python files in the repo and then use the OpenAI API for Codex model to get a brief description of the code in each file.

## Usage
```
python code_explainer.py \ 
  --repo_url <http code path for a repo url> \
  --output_file <json output file path>
```
