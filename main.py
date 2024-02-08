import json
import strawberry
import requests
from typing import Optional
import re
import codebleu
import subprocess
from RequestState import RequestState


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
        return get_llm_response(prompt, RequestState(prompt.prompt_type))
        # return dummy_llm_response(prompt)


def construct_prompt(content: str, state: RequestState) -> str:
    """
    A function to return a relevant prompt based on a given prompt_type and the contenet associated with it
    :param content: the content of the prompt to be constructed
    :param state: the current state of the request
    :return: the prompt to be used for the specific given prompt_type
    """
    prompt_type = state.get_prompt_type()
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
        if state.get_iteration() > 3:
            constructed_prompt = (
                "[INST] <<SYS>> You are a Java developer optimizing JUnit tests for clarity. <</SYS>> Your task "
                "is to make a previously written JUnit test more understandable. The returned understandable test "
                "must be between the [TEST] and [/TEST] tags. \n"
                f"Add comments to the code which explain what is happening and the "
                "intentions of what is being done."
                "Overall, it is the goal to have a more descriptive test.\n "
                "The previously written test to improve is between the [CODE] and [/CODE] tags.\n"
                f"[CODE]\n{content}\n[/CODE]\n")
        else:
            given_when_then = " with the Given, When, Then Structure" if state.is_first_run() else ""
            constructed_prompt = (
                "[INST] <<SYS>> You are a Java developer optimizing JUnit tests for clarity. <</SYS>> Your task "
                "is to make a previously written JUnit test more understandable. The returned understandable test "
                "must be between the [TEST] and [/TEST] tags. \n"
                f"Add comments{given_when_then} to the code which explain what is happening and the "
                "intentions of what is being done."
                "Only Change variable names to make them more relevant leaving the test data untouched."
                "Overall, it is the goal to have a more concise test which is "
                "both descriptive as well as relevant to the context. \n"
                "The previously written test to improve is between the [CODE] and [/CODE] tags.\n"
                f"[CODE]\n{content}\n[/CODE]\n")

    return constructed_prompt


def restart_llm():
    """A function to call the bash script which will restart the docker container of the LLM"""
    try:
        print("attempting_restart")
        subprocess.run(['./restart_llm_container.sh'])
    except:
        print("Something went wrong when trying to restart the LLM let's try again")
        restart_llm()

    print("Restart of the LLM successful - resuming regular processes")


def utilize_llm(prompt: str, state: RequestState, model: str = "codellama:7b-instruct") -> str:
    """
    A function to utilize an LLM available in Ollama by providing the prompt and the (optional) model to use
    :param state: the current state of the request
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
        "stream": False,
        "keep_alive": -1
    }
    state.increment_llm_calls()
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data), timeout=60)
    except requests.exceptions.Timeout:
        print("The LLM has been unresponsive for a while...\nRestarting the LLM")
        restart_llm()

    if response.status_code == 200:
        data = json.loads(response.text)
        return data["response"]
    else:
        print("There was an error while trying to send the request to the LLM, trying again...")
        return utilize_llm(prompt, state, model=model)


def validate_test_name(name: str) -> bool:
    """
    A function to validate that the name of the test is valid
    :param name: the name that is to be validated
    :return: whether the string is valid
    """
    invalid = ["@", "[", "]", "{", "}", ";", ":", "=", ",", "."]
    for char in invalid:
        if (char in name):
            return False

    if len(name.strip()) > 50 or len(name.strip()) < 5:
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
    """
    A method to validate whether the test method is valid by checking that is not exclusively comments
    :param body: The code to check for validity
    :return: a boolean indicating whether a test method is valid
    """
    # TODO : implement using ANTLR or Spoon
    code_split = body.split("\n")
    count_comment_lines = 0
    for line in code_split:
        for elem in ["Given", "When", "Then", "given", "when", "then", "And", "and", "Also", "also", "//"]:
            if elem in line.strip():
                count_comment_lines += 1
                break
    return count_comment_lines != len(code_split)


def comment_stripped_code(body: str):
    """
    A function to only get the code without the comments
    :param body: the code to remove the comments from
    :return: code with exclusively code and no comments
    """
    lines = body.split("\n")
    lines_stripped = []
    for line in lines:
        if "//" not in line.strip()[0:2]:
            lines_stripped.append(line)

    return "\n".join(lines_stripped)


def get_code_bleu_score(response_code, original_code):
    """
    A method to get the code bleu score for the generated code
    :param response_code: The response from the LLM without comments
    :param original_code: The original code without any improvements made
    :return: the score for the response
    """

    code_bleu_scores = codebleu.calc_codebleu([original_code], [response_code], lang="java",
                                              weights=(0.25, 0.25, 0.25, 0.25))
    print("Results for codebleu evaluation are: ")
    print(code_bleu_scores)
    return code_bleu_scores['codebleu']


def has_valid_brackets(code: str) -> bool | str:
    """
    A method which check whether all the brackets and parentheses are matched correctly and in the case the code
    is valid throughout, it tries to fix the brackets after the code has finished being processed
    :param code: code to evaluate the bracket correctness of
    :return: a boolean indicating whether a code piece is correct
    """

    stack = []

    matching_closing = {"}": "{", ")": "(", "]": "["}
    matching_opening = {"{": "}", "(": ")", "[": "]"}

    for char in code:
        if char in "{[(":
            stack.append(char)
            continue
        elif char in "}])":
            if not stack or stack[-1] != matching_closing[char]:
                return False
            stack.pop()
            continue

    if not stack:
        return True
    else:
        while stack:
            code = code + (matching_opening[stack.pop()])
            if code[-1] == ")":
                code += ";"
        return code


def parse_refined_test_method(code: str, original_code: str) -> str:
    """
    A method to refine the format of the extracted refined test method
    :param code: The code we want to refine
    :param original_code: The original code which was improved by the llm
    :return: The refined body of the test
    """
    # concatenating the different lines and returning the final string.
    body = get_code_body(code)
    valid = validate_refined_test_method_is_valid(body)
    if "try" in body and "catch" not in body:
        return None

    if "catch" in body and "try" not in body:
        return None

    # if "try" in body and "catch" in body:
    #     body = body + "\n}"

    score = get_code_bleu_score(comment_stripped_code(body), original_code)

    valid_brackets = has_valid_brackets(body)

    if isinstance(valid_brackets, str):
        body = valid_brackets
        valid_brackets = True

    if (re.search(r"public\s+void\s+(\w+)\s*\(([^)]*)\)", body) or
            re.search(r"import\s+(static\s+)?[\w\.]+(\.\*)?;", body)):
        return None

    for unwanted_token in ["@Test", "Given(", "When(", "Then("]:
        if unwanted_token in body:
            return None

    return body if (valid and score > 0.5 and valid_brackets) else None


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


def extract_answer(response: str, prompt_type: str, original_code: Optional[str] = None) -> str:
    """
    extracts the answer of the LLM based on the type of the prompt
    :param original_code: The original code which can be provided in the case where we are extracting refined test
    :param response: the complete response from teh LLM
    :param prompt_type: the type of the prompt according to which the answer is extracted
    :return: the extracted answer
    """
    regex_fallback = r'```(.*?)```'
    fallback_testname = r'^TESTNAME:\s*(.+)$'

    if prompt_type == "testname":
        regex_test = r'\[TESTNAME](.*?)\[/TESTNAME]'
    elif prompt_type == "testdata":
        regex_test = r'\[TESTDATA](.*?)\[/TESTDATA]'
    else:
        regex_test = r'\[TEST](.*?)\[/TEST]'

    try:
        extracted_answer = re.findall(regex_test, response, re.DOTALL)[(
            -1 if prompt_type == "testdata" or prompt_type == "testname" else 0
        )]
    except:
        try:
            extracted_answer = re.findall(regex_fallback, response, re.DOTALL)[(
                -1 if prompt_type == "testdata" else 0
            )]
            while extracted_answer[0] == '`':
                extracted_answer = extracted_answer[1:]
            while extracted_answer[-1] == '`':
                extracted_answer = extracted_answer[:-1]
            # extracted_answer = extracted_answer[3: -3]
            if "java" in extracted_answer[0:4]:
                extracted_answer = extracted_answer[4:]

        except:
            try:
                if prompt_type == "testname":
                    extracted_answer = re.findall(fallback_testname, response, re.MULTILINE)[-1]
                else:
                    raise Exception
            except:
                print("The format of the returned response from the LLM was invalid")
                return None

    print("\n\nThe extracted answer is:\n" + extracted_answer)

    if prompt_type == "testname":
        extracted_answer = parse_test_name(extracted_answer)
    elif prompt_type == "testdata":
        extracted_answer = parse_test_data(extracted_answer)
    else:
        extracted_answer = parse_refined_test_method(extracted_answer, original_code)

    return extracted_answer


def get_llm_response(prompt: Prompt, state: RequestState) -> Response:
    """
    Function to handle the communication with the LLM based on the implementation in the utilize_llm function

    :param state: the current state of the request
    :param prompt: the provided prompt by the user as a Prompt type containing the fields required
    :return: The response of the llm as a Response type
    """
    state.increment_iteration()
    if prompt.prompt_type not in ["testname", "testdata"] and state.get_iteration() > 5:
        print("\nThe LLM could not improve the provided code...\n\tReturning original code")
        state.end_request()
        print(state.__repr__())
        return Response(llm_response="// No Comments were added\n" + prompt.prompt_text)

    try:
        constructed_prompt = construct_prompt(prompt.prompt_text, state)
        print("The constructed prompt is:\n" + constructed_prompt)

        response = utilize_llm(constructed_prompt, state)
        print("\n\nThe unprocessed LLM response was:\n" + response)

        answer = extract_answer(response, prompt.prompt_type, prompt.prompt_text)

        if not answer:
            raise Exception
        state.end_request()
        print("\nThe final answer from LLM Server is:\n" + answer)
        print(state.__repr__())
        return Response(llm_response=answer)


    except:
        print("There was an Error!")
        print("Trying again with same prompt...")
        return get_llm_response(prompt, state)


schema = strawberry.Schema(query=Query)
