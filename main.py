import json
import strawberry
import requests
from typing import Optional
import re


# Global variables to configure the behavior of the script and the model used.
# USE_LOCAL_LLM flag determines whether to use a local model (with ollama) or an external API for LLM.

USE_LOCAL_LLM = True   # <- set this boolean to false if you don't want to use a local model

api_token = "hf_XXXXXXX"  # <- change this to your hugging_face_token
#model_id = "WizardLM/WizardCoder-3B-V1.0"  # <- change this to the model you want to use


model_id = "codellama/CodeLlama-7b-Instruct-hf"   # <- this is the model intended to be used but had to be commented out

@strawberry.input
class Prompt:
    prompt_text: str
    prompt_type: Optional[str] = None
    mut_signature_and_doc: Optional[str] = None


@strawberry.type
class Response:
    llm_response: str


@strawberry.type
class Query:
    @strawberry.field
    def prompt(self, prompt: Prompt) -> Response:
        """
        This is the prompt endpoint which can be used to prompt the llm from the EvoSuite part of the pipeline
        :param prompt: takes in a Prompt type and based on that calls the get_llm_response
        :return: the llm response of type Response containing the generated text by the llm.
        """
        return get_llm_response(prompt)


def get_llm_response(prompt: Prompt) -> Response:
    """
    Function to handle the communication with the LLM (either local or via Hugging Face API)
    based on the USE_LOCAL_LLM flag. Constructs the prompt and processes the response.

    :param prompt: the provided prompt by the user as a Prompt type containing the fields required
    :return: The response of the llm as a Response type
    """

    # This constructed prompt is based on the paper by meta on CodeLlama and how to design prompts for the model
    # based on the model in use and task specification at hand this construction should be adjusted accordingly

    constructed_prompt = (
                "[INST] <<SYS>> You are a Java developer optimizing JUnit tests for clarity. <</SYS>> Your task is to "
                "make a"
                "previously written JUnit test more understandable. The understandable test must be between the ["
                "TEST] and [/TEST] tags. Provide comments where necessary and rename variables to be understandable. "
                "The code to improve is between the [CODE] and [/CODE] tags. The method signature and javadoc of the "
                "method under test is given between the [SIGNATURE] and [/SIGNATURE] tags. Only provide the improved "
                "test[/INST]\n\n" +
                f"[CODE]\n{prompt.prompt_text}\n[/CODE]\n[SIGNATURE]\n{prompt.mut_signature_and_doc}\n[/SIGNATURE]\n")

    print(constructed_prompt)   # Debugging : Print constructed prmopt
    if not USE_LOCAL_LLM:
        # Handling communication with the Hugging Face API
        API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
        headers = {"Authorization": f"Bearer {api_token}"}

        payload = {
            'inputs': constructed_prompt,
            # 'parameters': {
            #     'max_new_tokens': 250,
            #     'top_p': 1,
            #     # any other parameters required
            # },
            'options': {
                'wait_for_model': False,
                # always handy for when models are not yet loaded
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        response_json = response.json()
        if 'error' in response_json:
            print("An error was encountered when trying to get a response")
            print(response_json)
            return Response(llm_response="No Response: Error Encountered")
        print(response_json)

        # Check if response_json is a list and has at least one element
        if isinstance(response_json, list) and len(response_json) > 0:
            # Assuming the first element in the list contains the desired data
            if 'generated_text' in response_json[0]:
                return Response(llm_response=response_json[0]['generated_text'])
            else:
                return Response(llm_response="No generated text found")
        else:
            return Response(llm_response="Invalid response format")
    else:
        # Handling communication with a local LLM instance

        API_URL = "http://localhost:11434/api/generate"
        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "model": "codellama",
            "prompt": constructed_prompt,
            "stream": False
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            try:
                regex_test = r'\[TEST](.*?)\[/TEST]'
                actual_response = data["response"]
                extracted_answer = re.findall(regex_test, actual_response, re.DOTALL)[0]
                # Extracting the specific response part from the entire response
                print(actual_response)
                return Response(llm_response=extracted_answer)
            except:
                return Response(llm_response="ERROR: Something Went Wrong When Extracting Response")
        else:
            print("Error:", response.status_code, response.text)


schema = strawberry.Schema(query=Query)
