import json
import strawberry
import requests
from typing import Optional
import re


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


def construct_prompt(content: str, prompt_type: str) -> str:
    """
    A function to return a relevant prompt based on a given prompt_type and the contenet associated with it
    :param content: the content of the prompt to be constructed
    :param prompt_type: the type of the prompt to be constructed
    :return: the prompt to be used for the specific given prompt_type
    """

    if prompt_type == "testname":
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
            f"[CODE]\n{content}\n[/CODE]\n"
        )
    elif prompt_type == "testdata":
        constructed_prompt = (
            "[INST] As a meticulous Java developer focused on enhancing the clarity and effectiveness "
            "of a test suite. Your task is to refine the test data within a given code fragment. Your goal is to "
            "make the data more descriptive and representative of the situation being tested. \n\n"
            "Please follow these steps:\n"
            "1. Carefully review the provided code snippet.\n"
            "2. Improve the test data by changing the primitive values and Strings (such as integers, doubles, strings,"
            " chars) to more illustrative examples.\n"
            "3. Place your Improved code between the [TESTDATA] and [/TESTDATA] tags when you are done with the "
            "previous steps.\n\n"
            "The code snippet you need to refine is between te [CODE] and [/CODE] tag.[/INST]\n"
            f"[CODE]\n{content}\n[/CODE]\n\n"
        )
    else:
        constructed_prompt = (
            "[INST] <<SYS>> You are a Java developer optimizing JUnit tests for clarity. <</SYS>> Your task "
            "is to make a previously written JUnit test more understandable. The returned understandable test "
            "must be between the [TEST] and [/TEST] tags. \n"
            "Add comments (with the Given, When, Then Structure) to the code which explain what is happening and the "
            "intentions of what is being done."
            "Only Change variable names to make them more relevant leaving the test data untouched."
            "Overall, it is the goal to have a more concise test which is "
            "both descriptive as well as relevant to the context. \n"
            "The previously written test to improve is between the [CODE] and [/CODE] tags.\n"
            f"[CODE]\n{content}\n[/CODE]\n")

    return constructed_prompt


def utilize_llm(prompt: str, model: str = "codellama:7b-instruct") -> str:
    """
    A function to utilize an LLM available in Ollama by providing the prompt and the (optional) model to use
    :param prompt: the prompt to send to the LLM
    :param model: the model to utilize which is set to codellam:7b-instruct by default
    :return: the response of the model
    """
    API_URL = "http://localhost:11434/api/generate"
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        data = json.loads(response.text)
        return data["response"]
    else:
        print("There was an error while trying to send the request to the LLM, trying again...")
        return utilize_llm(prompt, model)


def validate_test_name(name:str) -> bool:
    """
    A function to to validate that the name of the test is valid
    :param name: the name that is to be validated
    :return: whether the string is valid
    """
    invalid = ["@", "[", "]", "{", "}", ";", ":", "=", ",", "."]
    for char in invalid:
        if(char in name):
            return False

    if len(name.strip()) > 50:
        return False

    return True


def parse_test_name(extracted_answer: str) -> str:
    """
    A method to return the extracted test name in proper format
    :param extracted_answer: the base extracted response from the LLM
    :return: the test name in the intended format
    """
    chars_to_remove = " ()_"
    for char in chars_to_remove:
        extracted_answer = extracted_answer.replace(char, "")
    valid = validate_test_name(extracted_answer)
    return extracted_answer.strip() if valid else None


def get_code_body(code: str) -> str:
    """
    A method to extract purely the method body
    :param code: The code to extract only the code from
    :param mode: The type of the extracting
    :return:
    """
    # Splitting the input string into lines
    lines = code.split("\n")

    # Defining keywords and comment indicators
    keywords = {"import", "@Test", "@Timeout", "public", "void", "Class", "{", "}"}
    comment_indicators = {"*", "/*", "*/"}

    # Helper function to check if a line should be skipped
    def should_skip(line: str) -> bool:
        stripped_line = line.strip()
        if not stripped_line:
            return True  # Skip empty lines
        if any(stripped_line.startswith(indicator) for indicator in comment_indicators):
            return True  # Don't keep javadoc prior to method

        if any(keyword in stripped_line for keyword in keywords):
            return not "[]" in stripped_line  # take array declaration with the format type[]
                                                # name = new type[] {} into account
        return False

    # Removing lines from the top
    while lines and (len(lines[0].strip()) == 0 or should_skip(lines[0])):
        lines.pop(0)

    if len(lines) > 1 and "public" in lines[1]:
        lines.pop(1)

    # Removing lines from the bottom
    while lines and (len(lines[-1].strip()) == 0 or should_skip(lines[-1])):
        lines.pop()

    # Joining the remaining lines
    return "\n".join(line.strip() for line in lines)


def validate_refined_test_method_is_valid(body: str) -> bool:
    # TODO : implement using ANTLR or Spoon
    code_split = body.split("\n")
    count_comment_lines = 0
    for line in code_split:
        for elem in ["Given", "When", "Then", "given", "when", "then", "And", "and", "Also", "also", "//"]:
            if elem in line.strip():
                count_comment_lines += 1
                break
    return count_comment_lines != len(code_split)


def parse_refined_test_method(code: str) -> str:
    # concatenating the different lines and returning the final string.
    body = get_code_body(code)
    valid = validate_refined_test_method_is_valid(body)
    return body if (valid and "@Test" not in body) else None


def parse_test_data(extracted_answer: str) -> str:
    """
    A method to return the extracted test data in proper format
    :param extracted_answer: the base extracted response from the LLM
    :return: the test data statements in the intended format
    """
    extracted_answer = get_code_body(extracted_answer)
    if (extracted_answer and len(extracted_answer) > 4 and
            "java" in extracted_answer.strip().lower()[0:4]):
        extracted_answer = extracted_answer[4:-1]

    return extracted_answer.strip() if "@Test" not in extracted_answer else None


def extract_answer(response: str, prompt_type: str) -> str:
    """
    extracts the answer of the LLM based on the type of the promtp
    :param response: the complete response from teh LLM
    :param prompt_type: the type of the prompt according to which the answer is extracted
    :return: the extracted answer
    """
    regex_fallback = r'```java(?:[\s\S]*?)```'
    if prompt_type == "testname":
        regex_test = r'\[TESTNAME](.*?)\[/TESTNAME]'
    elif prompt_type == "testdata":
        regex_test = r'\[TESTDATA](.*?)\[/TESTDATA]'
    else:
        regex_test = r'\[TEST](.*?)\[/TEST]'

    try:
        extracted_answer = re.findall(regex_test, response, re.DOTALL)[(
            -1 if prompt_type == "testdata" else 0
        )]
    except:
        try:
            extracted_answer = re.findall(regex_fallback, response, re.DOTALL)[(
                -1 if prompt_type == "testdata" else 0
            )]
            extracted_answer = extracted_answer[3: -3]
            if "java" in extracted_answer[0:4]:
                extracted_answer = extracted_answer[4:]

        except:
            print("The format of the returned response from the LLM was invalid")
            return None

    print("\n\nThe extracted answer is:\n" + extracted_answer)

    if prompt_type == "testname":
        extracted_answer = parse_test_name(extracted_answer)
    elif prompt_type == "testdata":
        extracted_answer = parse_test_data(extracted_answer)
    else:
        extracted_answer = parse_refined_test_method(extracted_answer)

    return extracted_answer


def get_llm_response(prompt: Prompt) -> Response:
    """
    Function to handle the communication with the LLM (either local or via Hugging Face API)
    based on the USE_LOCAL_LLM flag. Constructs the prompt and processes the response.

    :param prompt: the provided prompt by the user as a Prompt type containing the fields required
    :return: The response of the llm as a Response type
    """

    try:
        constructed_prompt = construct_prompt(prompt.prompt_text, prompt.prompt_type)
        print("The constructed prompt is:\n" + constructed_prompt)

        response = utilize_llm(constructed_prompt)
        print("\n\nThe unprocessed LLM response was:\n" + response)

        answer = extract_answer(response, prompt.prompt_type)
        if not answer:
            raise Exception
        print("\nThe final answer from LLM Server is:\n" + answer)

        return Response(llm_response=answer)


    except:
        print("There was an Error!")
        print("Trying again with same prompt...")
        return get_llm_response(prompt)


schema = strawberry.Schema(query=Query)

# =====================
# Some tests
# =====================