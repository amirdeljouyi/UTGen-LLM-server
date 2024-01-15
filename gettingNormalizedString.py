import json
import re

import requests

USE_LOCAL_LLM = True

code = """
  @Test
  public void getPetsTest() throws Exception{
      Owner subject = new Owner();
      Pet max = new Pet();
      PetType dog = new PetType();
      dog.setName("dog");
      max.setType(dog);
      max.setName("Max");
      max.setBirthDate(LocalDate.now());
      max.setId(1);
      subject.addPet(max);

      Pet getPet = subject.getPet("Max");

      assertThat("Max", getPet.toString());
  }\n"""
code = repr(code)


def get_llm_response(prompt, type):
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
    if type == "testname":
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
            f"[CODE]\n{prompt}\n[/CODE]\n"
        )

        regex_test = r'\[TESTNAME](.*?)\[/TESTNAME]'

    elif type == "testdata":
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
            f"[CODE]\n{prompt}\n[/CODE]\n\n"
        )
        regex_test = r'\[TESTDATA](.*?)\[/TESTDATA]'
    else:
        constructed_prompt = (
            "[INST] <<SYS>> You are a Java developer optimizing JUnit tests for clarity. <</SYS>> Your task "
            "is to make a previously written JUnit test more understandable. One the returned understandable test "
            "must be between the [TEST] and [/TEST] tags. Provide descriptive "
            "comments where necessary and rename variables to ones that are more relevant. Do not improve the data "
            "used in the tests. Overall, it is the goal to have a more concise test which is both descriptive as well "
            "as relevant to the context. "
            "The previously written test to improve is between the [CODE] and [/CODE] tags."
            f"[CODE]\n{prompt}\n[/CODE]\n")
        regex_test = r'\[TEST](.*?)\[/TEST]'

    print(constructed_prompt)  # Debugging : Print constructed prmopt
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

            return extracted_answer
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

                extracted_answer
            except:
                return "ERROR: Something Went Wrong When Extracting Response"
    else:
        print("Error:", response.status_code, response.text)

for i in range(5):
    print(f"\n\nThis are the results from run {i}\n\n")
    print(get_llm_response(code, "codegen"))



