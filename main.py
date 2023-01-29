import colorama

from code_embedder import CodeEmbeddingIndexer
from format_utils import (change_print_color, clear_output, cprint,
                          custom_print_code, pretty_print, print_table)
from openai_utils import OpenAIWrapper
from python_parser import PythonParser
from repository import GitRepo


def get_repo_url():
    cprint("Enter a git repo http url: ", is_input=True)
    repo_url = input()
    return repo_url

def input_with_options(options):
    print()
    print("*"*50)
    cprint("Choose one option below: ")
    for index, opt in enumerate(options):
        cprint(f"{index+1}. {opt}")
    print("*"*50)
    print()
    return input().strip()


def main():
    # Get Repo URL, Clone the Repo
    clear_output()
    change_print_color(colorama.Fore.LIGHTYELLOW_EX)
    repo_url = get_repo_url()
    print()

    change_print_color(colorama.Fore.LIGHTGREEN_EX)
    repo = GitRepo(repo_url)
    repo.clone()
    print()

    # Parse the repo, Parse all python functions
    parser = PythonParser(repo.repo_path)
    code_funcs = parser.get_all_functions()
    print()

    # Get Embeddings for all functions
    # Generate a NN Search Index
    change_print_color(colorama.Fore.LIGHTGREEN_EX)
    indexer = CodeEmbeddingIndexer(repo.repo_path, code_funcs)
    indexer.create_index()
    print()

    wrapper = OpenAIWrapper()

    while True:
        change_print_color(colorama.Fore.LIGHTYELLOW_EX)

        option = input_with_options([
            "Search for functions using natural language",
            "Select a function by name",
            "Exit"
        ])

        clear_output()

        if option == "3":
            cprint("Exiting ...")
            break

        if option == "1":
            change_print_color(colorama.Fore.LIGHTYELLOW_EX)
            cprint("Enter a natural language search query: ", is_input=True)
            query = input()

            change_print_color(colorama.Fore.LIGHTCYAN_EX)
            code_funcs_neighbors, distances = indexer.search_index(query, 3)
            table = [[x['relative_filepath'], x['function_name'], y] for x,y in zip(code_funcs_neighbors, distances)]
            headers = ['relative_filepath', 'function_name', 'embedding_distance']
            print_table(table, headers)

        if option == "2":
            change_print_color(colorama.Fore.LIGHTYELLOW_EX)
            cprint("Enter a function name to search: ", is_input=True)
            query = input()
            change_print_color(colorama.Fore.LIGHTCYAN_EX)
            selected_code_func = None
            for code_func in code_funcs:
                if code_func["function_name"] == query:
                    selected_code_func = code_func
                    break
            
            if not selected_code_func:
                cprint("Could not find a function with that name")
            else:
                cprint("Found function")
                custom_print_code(selected_code_func, include_code=True)
                while True:
                    change_print_color(colorama.Fore.LIGHTYELLOW_EX)
                    sub_option = input_with_options(
                        [
                            "What would you like to know about this function? Insert a custom prompt.", 
                            "Provide an explanation of the function",
                            "Generate unit test for function",
                            "Refactor function to be more modular", 
                            "Go back to Main Menu",
                        ]
                    )
                    change_print_color(colorama.Fore.LIGHTMAGENTA_EX)
                    if sub_option == "5":
                        break
                    else:
                        print("-"*100)
                        if sub_option == "1":
                            custom_prompt = input()
                            cprint(wrapper.custom_gpt_call_code(selected_code_func["code"], custom_prompt))
                        elif sub_option == "2":
                            cprint(wrapper.explain_code(selected_code_func["code"]))
                        elif sub_option == "3":
                            cprint(wrapper.generate_unit_test(selected_code_func["code"]))
                        elif sub_option == "4":
                            result = wrapper.refactor_function(selected_code_func["code"])
                            pretty_print(result)
                        print("-"*100)


if __name__ == '__main__':
    main()
