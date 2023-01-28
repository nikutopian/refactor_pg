# Repository for Refactor Project

## Installation
```
conda create --env refactor_env
conda activate refactor_env
conda install scipy scikit-learn plotly matplotlib
pip install -r requirements.txt
```

## Description
The initial setup does the following: 
1. Download a git repository locally
2. Find all the python files in the repo and parse them to find all functions 
3. Generate embeddings for all python functions using OpenAI models. 
4. Create a Nearest Neighbor Search Index with all the embeddings.

The functionalities supported by the tool includes:
1. Search functions using a natural language description (using Embeddings)
2. Search functions by exact name. (simple string match)
3. Generate a brief explanation of a function. (using GPT3)
4. Generate unit tests for a function. (using GPT3)
5. Refactor a function to be more compact. (using GPT3)

## Usage
```
python main.py
```
