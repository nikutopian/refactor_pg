import argparse
import os
from pprint import pprint

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

from prettytable import PrettyTable, PLAIN_COLUMNS

import pandas as pd

from code_embedder import CodeEmbeddingIndexer
from openai_utils import OpenAIWrapper
from python_parser import PythonParser
from repository import GitRepo

clear_output = lambda: os.system('cls' if os.name=='nt' else 'clear')

def pretty_print(code):
    print(highlight(code, PythonLexer(), TerminalFormatter()))

def get_repo_url():
    repo_url = input("Enter a git repo http url: ")
    return repo_url

def custom_print_code(code_func, include_code=False):
    print(f"{code_func['filepath']}::{code_func['function_name']}")
    if include_code:
        print("-"*100)
        pretty_print(code_func["code"])
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

        clear_output()

        if option == "3":
            print("Exiting ...")
            break

        if option == "1":
            query = input("Enter a function search query: ")
            code_funcs_neighbors, distances = indexer.search_index(query, 3)
            code_paths = map(lambda c: f"{c['filepath']}::{c['function_name']}", code_funcs_neighbors)
            table = PrettyTable()
            table.set_style(PLAIN_COLUMNS)
            table.field_names = ["Function Path", "Distance Metric"]
            table.add_rows(zip(code_paths, distances))
            print("\n"*5)
            print(table)
            print("\n"*5)
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
                            result = wrapper.refactor_function(selected_code_func["code"])
                            pretty_print(result)
                        print("-"*100)


if __name__ == '__main__':
    main()
