import strawberry
import requests
from typing import Optional

# from transformers import AutoModelForCausalLM, AutoTokenizer

api_token = "hf_XXXXXXX"  # <- change this to your hugging_face_token
model_id = "WizardLM/WizardCoder-3B-V1.0" # <- change this to the model you want to use


# model_id = "codellama/CodeLlama-7b-Instruct-hf" # <- this is the model intended to be used but had to be commented out

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
    defined function to communicate with the hugging face api to prompt the llm and get the response

    :param prompt: the provided prompt by the user as a Prompt type containing the fields required
    :return: The response of the llm as a Response type
    """
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {api_token}"}

    # This constructed prompt is based on the paper by meta on CodeLlama and how to design prompts for the model
    # based on the model in use and task specification at hand this construction should be adjusted accordingly
    # constructed_prompt = ("[INST]Your task is to make a previously written JUnit test more understandable." +
    #                       "The understandable test must be between the [TEST] and [/TEST] tags. Provide comments" +
    #                       " where necessary and rename variable to be understandable. The code to improve is between" +
    #                       " the [CODE] and [/Code] tags. The method signature and javadoc of the method under test is" +
    #                       " given between the [SIGNATURE] and [/SIGNATURE] tags. [/INST]\n\n" +
    #                       f"[CODE]\n{prompt.prompt_text}\n[/CODE]\n[SIGNATURE]\n{prompt.mut_signature_and_doc}\n[/SIGNATURE]\n")

    # The adapted prompt for wizard coder
    # constructed_prompt = ("Below is an instruction that describes a task."
    #                       "Write a response that appropriately completes the request."
    #                       "\n\n### Instruction:Your task is to make a previously written JUnit test more "
    #                       "understandable. Provide comments where necessary and rename variable to be understandable."
    #                       "The code to improve can be found below the CODE tag. The method signature and javadoc"
    #                       " of the method under test is below the tag SIGNATURE.\n\n"
    #                       f"###CODE\n{prompt.prompt_text}\n\n###SIGNATURE\n{prompt.mut_signature_and_doc}\n\n\n### "
    #                       f"Response:")
    constructed_prompt = ("Below is an instruction that describes a task. Write a response that appropriately "
                          "completes the request.\n\n### Instruction:\nWrite a Java method that takes two numbers and "
                          "calculates the power of the first number to the second number in a recursive way\n\n### "
                          "Response:")

    # the payload sent to hf along with the api call to generate the desired output, along with additional parameters
    # and options if required, if not these can be commented out.
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

    print(constructed_prompt)
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
    # print(constructed_prompt)
    # return Response(constructed_prompt)


schema = strawberry.Schema(query=Query)
