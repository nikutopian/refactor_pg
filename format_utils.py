import os
import colorama
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from tabulate import tabulate

colorama.init(autoreset=True)
CURRENT_COLOR = colorama.Fore.LIGHTWHITE_EX

def clear_output():
    os.system('cls' if os.name=='nt' else 'clear')

def change_print_color(color):
    global CURRENT_COLOR
    CURRENT_COLOR = color

def cprint(str, is_input=False):
    print(CURRENT_COLOR + str, end='' if is_input else '\n')

def pretty_print(code):
    print(highlight(code, PythonLexer(), TerminalFormatter()))

def custom_print_code(code_func, include_code=False):
    cprint(f"{code_func['relative_filepath']}::{code_func['function_name']}")
    if include_code:
        print("-"*100)
        pretty_print(code_func["code"])
        print("-"*100)

def print_table(table, headers):
    print(
        colorama.Fore.LIGHTWHITE_EX + 
        tabulate(table, headers, tablefmt="rounded_grid")
    )
