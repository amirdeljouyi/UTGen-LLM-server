import json


def load_json_data(file_path):
    """
    Load JSON data from a given file path.

    :param file_path: Path to the JSON file.
    :return: The data contained in the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def find_mut_for_tests(test_details, project_details):
    """
    Find the corresponding Method Under Test (MUT) for each test method in the test details.

    :param test_details: List of test methods from the test details file.
    :param project_details: List of project details from the project details file.
    :return: A list of tuples, each containing the test method and its corresponding MUT.
    """
    # Flattening the project details to ease the search of methods by ID
    method_details = {}
    for entry in project_details:
        for cls in entry['classes']:
            for method in cls['methods']:
                method_details[method['id']] = method

    # Finding the MUT for each test
    test_with_mut = []
    for test in test_details:
        mut_id = test['source_method_id']
        mut = method_details.get(mut_id, None)
        if mut:
            test_with_mut.append((test, mut))

    return test_with_mut


def construct_prompt(test_mut_pair):
    """
    Constructs a prompt for each test-MUT pair. Adjusts the content based on the availability of MUT and its javadoc.

    :param test_mut_pair: A tuple containing the test method and its corresponding MUT.
    :return: A tuple containing the original test-MUT pair and the constructed prompt.
    """
    test_method, mut = test_mut_pair

    # Constructing the prompt parts
    prompt_inst = (
        "[INST] <<SYS>> You are a Java developer optimizing JUnit tests for clarity. <</SYS>> Your task is to "
        "make a previously written JUnit test more understandable. The understandable test must be between the ["
        "TEST] and [/TEST] tags. Provide comments where necessary and rename variables and the test name to be "
        "understandable. The previously written test to improve is between the [CODE] and [/CODE] tags. "
        "The method signature, implementation and javadoc of the method under test is given between the [METHOD] and "
        "[/METHOD] tags.[/INST]\n\n"
    )
    prompt_code = f"[CODE]\n{test_method['source_code']}\n[/CODE]\n"

    # Adjusting for the availability of MUT and its javadoc
    mut_signature_and_doc = f"{mut['code']}"
    if mut.get('javadoc'):
        mut_signature_and_doc = f"\n{mut['javadoc']}" + mut_signature_and_doc
    prompt_method = f"[METHOD]\n{mut_signature_and_doc}\n[/METHOD]\n"

    # Combining the parts into one prompt
    constructed_prompt = prompt_inst + prompt_code + prompt_method

    return {
        "prompt_components": {
            "mut_package": test_method["mut_package_name"],
            "test_method_name": test_method["test_method_name"],
            "extracted_mut_name": test_method["mut_in_name"],
            "test_source_code": test_method["source_code"],
            "mut": mut
        },
        "prompt": constructed_prompt
    }


method_file_path = "./java_project_details_petclinic.json"
test_file_path = "./java_project_test_details_petclinic.json"

project_details = load_json_data(method_file_path)
test_details = load_json_data(test_file_path)

test_mut_pairs = find_mut_for_tests(test_details=test_details, project_details=project_details)
pairs_with_prompts = []
for pair in test_mut_pairs:
    pairs_with_prompts.append(construct_prompt(pair))

prompt_json = json.dumps(pairs_with_prompts, indent=4)

output_file_path = "prompts_with_details_petclinic.json"
with open(output_file_path, "w") as output_file:
    output_file.write(prompt_json)

