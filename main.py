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
        # return dummy_llm_response(prompt)

def get_llm_response(prompt: Prompt) -> Response:
    """
    Function to handle the communication with the LLM (either local or via Hugging Face API)
    based on the USE_LOCAL_LLM flag. Constructs the prompt and processes the response.

    :param prompt: the provided prompt by the user as a Prompt type containing the fields required
    :return: The response of the llm as a Response type
    """

    # This constructed prompt is based on the paper by meta on CodeLlama and how to design prompts for the model
    # based on the model in use and task specification at hand this construction should be adjusted accordingly

    # constructed_prompt = (
    #             "[INST] <<SYS>> You are a Java developer optimizing JUnit tests for clarity. <</SYS>> Your task is to "
    #             "make a"
    #             "previously written JUnit test more understandable. The understandable test must be between the ["
    #             "TEST] and [/TEST] tags. Provide comments where necessary and rename variables and the test name to be "
    #             "understandable."
    #             "The previously written test to improve is between the [CODE] and [/CODE] tags. The method signature "
    #             "and javadoc of the"
    #             "method under test is given between the [SIGNATURE] and [/SIGNATURE] tags.[/INST]\n\n" +
    #             f"[CODE]\n{prompt.prompt_text}\n[/CODE]\n[SIGNATURE]\n{prompt.mut_signature_and_doc}\n[/SIGNATURE]\n")
    if prompt.prompt_type == "testname":
        # constructed_prompt = (
        #     "[INST] suggest an understandable test method name which is descriptive for the provided Java code. "
        #     "the name should be exclusively UpperCamelCase, where each word begins with a capital letter."
        #     "Put the understandable test method name in between the [TESTNAME] and [/TESTNAME] tags. "
        #     "The test to name is between the [CODE] and [/CODE] tags.[/INST]\n"
        #     f"[CODE]\n{prompt.prompt_text}\n[/CODE]\n")
        constructed_prompt = (
            "[INST] As a detail-oriented developer, your task is to analyze the provided Java code and deduce a "
            "descriptive test method name. Follow these steps:\n"
            "1. Carefully read the Java code between the [CODE] tags.\n"
            "2. Identify the primary functionality or purpose of the test.\n"
            "3. Formulate a test method name that succinctly captures this functionality, adhering to lowerCamelCase "
            "conventions.\n"
            "4. Place your suggested test method name between the [TESTNAME] and [/TESTNAME] tags, ensuring it is "
            "clear and precise without additional descriptions.\n"
            "Remember, your focus is on clarity and precision. Use your expertise to provide a meaningful and "
            "appropriate name.[/INST]\n"
            f"[CODE]\n{prompt.prompt_text}\n[/CODE]\n"
        )

        regex_test = r'\[TESTNAME](.*?)\[/TESTNAME]'

    elif prompt.prompt_type == "testdata":
        constructed_prompt = (
            "[INST] As a meticulous Java developer focused on enhancing the clarity and effectiveness "
            "of a test suite. Your task is to refine the test data within a given code fragment. Your goal is to "
            "make the data more descriptive and representative of the situation being tested. \n\n"
            "Please follow these steps:\n"
            "1. Carefully review the provided code snippet.\n"
            "2. Identify the key functionality the test is addressing.\n"
            "3. Improve the test data by changing the primitive values and Strings (such as integers, doubles, strings,"
            " chars) to more illustrative examples.\n"
            "4. Place your Improved code between the [TESTDATA] and [/TESTDATA] tags when you are done with the "
            "previous steps.\n\n"
            "Remember, your modifications should only involve the test data, not the code structure or logic. "
            "The code snippet you need to refine is between te [CODE] and [/CODE] tag.[/INST]\n"
            f"[CODE]\n{prompt.prompt_text}\n[/CODE]\n\n"
        )
        regex_test = r'\[TESTDATA](.*?)\[/TESTDATA]'
    else:
        constructed_prompt = (
            "[INST] <<SYS>> You are a Java developer optimizing JUnit tests for clarity. <</SYS>> Your task "
            "is to make a previously written JUnit test more understandable. The returned understandable test "
            "must be between the [TEST] and [/TEST] tags, and do not put it in wrapper class. Provide comments where "
            "necessary, rename variables,"
            "improve test data, and rename the test name to be understandable."
            "The previously written test to improve is between the [CODE] and [/CODE] tags."
            f"[CODE]\n{prompt.prompt_text}\n[/CODE]\n")
        regex_test = r'\[TEST](.*?)\[/TEST]'


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
            "model": "codellama:7b-instruct",
            "prompt": constructed_prompt,
            "stream": False
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps(data))


        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            try:
                actual_response = data["response"]
                print(actual_response)
                # Extracting the specific response part from the entire response
                extracted_answer = re.findall(regex_test, actual_response, re.DOTALL)[0]

                if prompt.prompt_type == "testname":
                    chars_to_remove = " ()_"
                    for char in chars_to_remove:
                        extracted_answer = extracted_answer.replace(char, "")
                elif prompt.prompt_type == "testdata":
                    extracted_answer = re.findall(regex_test, actual_response, re.DOTALL)[-1]
                    print("The extracted answer is:\n")
                    print(repr(extracted_answer))

                    split_string = extracted_answer.split("\n")
                    answer_without_comments = []
                    for i, line in enumerate(split_string):
                        if "//" not in line:
                            answer_without_comments.append(line)
                    extracted_answer = "\n".join(answer_without_comments)


                return Response(llm_response=extracted_answer)
            except:
                try:
                    regex_test = r'```(?:java )?(.*?)```'
                    actual_response = data["response"]
                    print(actual_response)
                    # Extracting the specific response part from the entire response
                    extracted_answer = re.findall(regex_test, actual_response, re.DOTALL)[0]
                    if prompt.prompt_type == "testname":
                        chars_to_remove = " ()_"
                        for char in chars_to_remove:
                            extracted_answer = extracted_answer(char, "")
                    elif prompt.prompt_type == "testdata":
                        extracted_answer = re.findall(regex_test, actual_response, re.DOTALL)[-1]
                        print("The extracted answer is:\n")
                        print(repr(extracted_answer))

                        split_string = extracted_answer.split("\n")
                        answer_without_comments = []
                        for i, line in enumerate(split_string):
                            if "//" not in line:
                                answer_without_comments.append(line)
                        extracted_answer = "\n".join(answer_without_comments)

                    return Response(llm_response=extracted_answer)
                except:
                    return Response(llm_response="ERROR: Something Went Wrong When Extracting Response")
        else:
            print("Error:", response.status_code, response.text)

def dummy_llm_response(prompt: Prompt) -> Response:
    return Response(llm_response=prompt.prompt_text)


schema = strawberry.Schema(query=Query)
