import os
import subprocess
import re 
import colorama

BASE_PATH = os.path.expanduser("~/data/repos/")
colorama.init(autoreset=True)

class GitRepo:
    def __init__(self, repo_url: str):
        if not os.path.exists(BASE_PATH):
            os.makedirs(BASE_PATH)
        self.repo_url = repo_url
        self.repo_path = os.path.join(BASE_PATH, repo_url.split("/")[-1])

    def clone(self):
        if os.path.exists(self.repo_path):
            print(colorama.Fore.LIGHTBLUE_EX+"Git repo already cloned locally")
        else:
            print(colorama.Fore.LIGHTBLUE_EX+"Cloning Git repo ...")
            subprocess.run(["git", "clone", self.repo_url, self.repo_path])
        print(colorama.Fore.LIGHTBLUE_EX+f"Git repo cloned at: {self.repo_path}")

    def list_files(self, filter=".*\.py$"):
        current_path =  os.getcwd()
        os.chdir(self.repo_path)
        files = subprocess.run(["git", "ls-files"], capture_output=True)
        os.chdir(current_path)
        all_files = files.stdout.decode().strip().split('\n')
        all_files = [os.path.join(self.repo_path, x) for x in all_files if not re.match("tests", x)]
        if filter:
            all_files = [x for x in all_files if re.match(filter, x)]
        return all_files