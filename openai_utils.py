import os

import openai

MODEL_NAME = "code-davinci-002"

class OpenAIWrapper:
    def __init__(self) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def __process_result(self, response):
        return response.get("choices", [{}])[0].get("text")

    def explain_code(self, code_string):
        prompt_suffix = "\n\n# Brief Explanation of what the code above does \n#"
        prompt_text = code_string + prompt_suffix

        response = openai.Completion.create(
            model=MODEL_NAME,
            prompt=prompt_text,
            temperature=0.1,
            max_tokens=512,
            top_p=1.0,
            frequency_penalty=0.3,
            presence_penalty=0.1
        )

        return self.__process_result(response)
