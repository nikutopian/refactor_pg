import argparse
import os
from pprint import pprint

import pandas as pd

from code_embedder import CodeEmbeddingIndexer
from openai_utils import OpenAIWrapper
from python_parser import PythonParser
from repository import GitRepo

def get_repo_url():
    repo_url = input("Enter a git repo http url: ")
    return repo_url

def custom_print_code(code_func, include_code=False):
    print(f"{code_func['filepath']}::{code_func['function_name']}")
    if include_code:
        print("-"*100)
        print(code_func["code"])
        print("-"*100)

def main():

    repo_url = get_repo_url()
    repo = GitRepo(repo_url)
    repo.clone()

    parser = PythonParser(repo.repo_path)
    code_funcs = parser.get_all_functions()

    indexer = CodeEmbeddingIndexer(repo.repo_path, code_funcs)
    indexer.create_index()

    wrapper = OpenAIWrapper()

    while True:
        print("-"*100)

        option = input("""Choose one option below:
        1. Search for functions using natural language
        2. Select a function
        3. Exit\n""").strip()

        if option == "3":
            print("Exiting ...")
            break

        if option == "1":
            query = input("Enter a function search query: ")
            code_funcs_neighbors, distances = indexer.search_index(query, 3)
            for code_funcs_neighbor, distance in zip(code_funcs_neighbors, distances):
                custom_print_code(code_funcs_neighbor)
                print(f"Distance metric: {distance}")
            print("-"*100)

        if option == "2":
            query = input("Enter a function name: ")
            selected_code_func = None
            for code_func in code_funcs:
                if code_func["function_name"] == query:
                    selected_code_func = code_func
                    break
            
            if not selected_code_func:
                print("Could not find a function with that name")
            else:
                print("Found function")
                custom_print_code(selected_code_func, include_code=True)
                while True:
                    sub_option = input("""Choose one option below:
                    1. What would you like to know about this function? Insert a custom prompt.
                    2. Provide an explanation of the function
                    3. Generate unit test for function
                    4. Refactor function to be more compact
                    5. Go back to Main Menu\n""").strip()
                    if sub_option == "5":
                        break
                    else:
                        print("-"*100)
                        if sub_option == "1":
                            custom_prompt = input()
                            print(wrapper.custom_gpt_call_code(selected_code_func["code"], custom_prompt))
                        elif sub_option == "2":
                            print(wrapper.explain_code(selected_code_func["code"]))
                        elif sub_option == "3":
                            print(wrapper.generate_unit_test(selected_code_func["code"]))
                        elif sub_option == "4":
                            print(wrapper.refactor_function(selected_code_func["code"]))
                        print("-"*100)


if __name__ == '__main__':
    main()
