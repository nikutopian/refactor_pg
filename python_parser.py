# Code derived from https://beta.openai.com/docs/guides/embeddings/use-cases
import os
from glob import glob
from format_utils import cprint

class PythonParser():

    def __init__(self, code_root):
        self.code_root = code_root
        self.code_files = self.__walk_code_files()
        cprint("Total number of python files: " + str(len(self.code_files)))

    def __walk_code_files(self):
        assert self.code_root is not None
        return [y for x in os.walk(self.code_root) for y in glob(os.path.join(x[0], '*.py'))]

    def get_all_functions(self):
        assert self.code_files is not None and len(self.code_files) > 0, \
            "Double check that root directory contains python files."

        all_funcs = []
        for code_file in self.code_files:
            funcs = list(self.get_functions(code_file))
            for func in funcs:
                all_funcs.append(func)

        cprint("Total number of python functions extracted: " + str(len(all_funcs)))

        return all_funcs


    def get_function_name(self, code: str):
        """
        Extract function name from a line beginning with "def "
        """
        assert code.startswith("def ")
        return code[len("def "): code.index("(")]

    def get_until_no_space(self, all_lines, i) -> str:
        """
        Get all lines until a line outside the function definition is found.
        """
        ret = [all_lines[i]]
        for j in range(i + 1, i + 10000):
            if j < len(all_lines):
                if len(all_lines[j]) == 0 or all_lines[j][0] in [" ", "\t", ")"]:
                    ret.append(all_lines[j])
                else:
                    break
        return "\n".join(ret)

    def get_functions(self, filepath):
        """
        Get all functions in a Python file.
        """
        whole_code = open(filepath).read().replace("\r", "\n")
        all_lines = whole_code.split("\n")
        for i, l in enumerate(all_lines):
            if l.startswith("def "):
                code = self.get_until_no_space(all_lines, i)
                function_name = self.get_function_name(code)
                # skip test functions
                if function_name.startswith("test_"):
                    continue
                yield {"code": code, "function_name": function_name, "filepath": filepath, "relative_filepath": filepath.replace(self.code_root, "")}

