import os

import openai

MODEL_NAME = "code-davinci-002"

class OpenAIWrapper:
    def __init__(self) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def __process_result(self, response):
        return response.get("choices", [{}])[0].get("text")
    
    def custom_gpt_call_code(self, code_string, user_prompt):
        prompt_text = code_string + "\n\"\"\"\n" + user_prompt + "\n"
        response = openai.Completion.create(
            model=MODEL_NAME,
            prompt=prompt_text,
            temperature=0.05,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.2,
            presence_penalty=0.1
        )
        return self.__process_result(response)

    def explain_code(self, code_string):
        prompt_suffix = "\"\"\"\nHere's what the above python function is doing:\n1."
        prompt_text = code_string + prompt_suffix

        response = openai.Completion.create(
            model=MODEL_NAME,
            prompt=prompt_text,
            temperature=0.05,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.2,
            presence_penalty=0.1
        )

        return "1." + self.__process_result(response)

    def generate_unit_test(self, code_string):
        prompt_suffix = "\"\"\"\nGenerate unit tests for the python function above.\n\"\"\""
        prompt_text = code_string + prompt_suffix

        response = openai.Completion.create(
            model=MODEL_NAME,
            prompt=prompt_text,
            temperature=0.05,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.2,
            presence_penalty=0.1
        )

        return self.__process_result(response)

    def refactor_function(self, code_string):
        prompt_suffix = "\"\"\"\nRefactor the python function above to be more compact and DRY.\n\"\"\""
        prompt_text = code_string + prompt_suffix

        response = openai.Completion.create(
            model=MODEL_NAME,
            prompt=prompt_text,
            temperature=0.05,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.2,
            presence_penalty=0.1
        )

        return self.__process_result(response)
