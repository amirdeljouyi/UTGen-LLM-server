import os
import re
import json
import javalang


def find_method_id(methods_file_path, package_name, method_name):
    """
    Function to find the ID of a method given a package name and method name in the provided JSON data.

    :param json_data: List of package details in JSON format.
    :param package_name: Name of the package to search for.
    :param method_name: Name of the method to search for.
    :return: ID of the method if found, otherwise None.
    """
    with open(methods_file_path, 'r') as methods:
        json_data = json.load(methods)

    for package in json_data:
        if package['package_name'] == package_name:
            for cls in package['classes']:
                for method in cls['methods']:
                    if method['method_name'] == method_name:
                        return method['id']
    return None


def extract_lines_from_file(file_path, start_line, end_line):
    """
    Extracts lines from a file given the start and end line numbers.

    :param file_path: Path to the file.
    :param start_line: The starting line number (inclusive).
    :param end_line: The ending line number (inclusive).
    :return: String containing the extracted lines.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extracting the specified range of lines
    # Note: Line numbers in a file are 1-based, but list indices in Python are 0-based.
    extracted_lines = lines[start_line - 1:end_line]
    return ''.join(extracted_lines)

def parse_test_method_name(method_name):
    """
    Simplified parsing of the test method name to extract the method under test (MUT).
    """
    # Remove the prefix 'test' or 'testCreates'\
    orig_name = method_name
    method_name = re.sub(r'^test(Creates)?', '', method_name)

    # Find the position of any of the keywords and cut off the string before it
    keywords = ['Taking', 'Returning', 'Where', 'Throws', 'And']
    for keyword in keywords:
        keyword_position = method_name.find(keyword)
        if keyword_position != -1:
            method_name = method_name[:keyword_position]
            break
    if not "Creates" in orig_name and method_name:
        method_name = method_name[0].lower() + method_name[1:]

    return method_name.strip()


def process_test_file(file_path, method_file_path):
    """
    Process a single Java test file to extract test methods and their details.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    tree = javalang.parse.parse(content)

    # Extract package name
    package_name = tree.package.name if tree.package else None
    test_methods = []

    for _, class_node in tree.filter(javalang.tree.ClassDeclaration):
        for method in class_node.methods:
            start_line, _ = method.position
            end_line = start_line  # Initialize end_line as start_line

            # Find the end line of the method
            if method.body:
                for statement in method.body:
                    if hasattr(statement, 'position') and statement.position:
                        end_line = max(end_line, statement.position.line)

            if any(isinstance(anno, javalang.tree.Annotation) and anno.name == 'Test' for anno in method.annotations):
                method_details = parse_test_method_name(method.name)

                if method_details:
                    # Extract the source code of the test method (similar to the earlier approach)
                    test_method_source_code = extract_lines_from_file(file_path, start_line - 1, end_line + 1)

                    # Find the corresponding source method ID
                    # source_method_id = find_source_method_id(java_project_details, method_details['mut'])

                    if ".evosuite" in package_name:
                        package_name = package_name.replace(".evosuite", "")

                    source_method_id = find_method_id(method_file_path, package_name, method_details)

                    test_methods.append({
                        "mut_package_name": package_name,
                        "test_method_name": method.name,
                        "mut_in_name": method_details,
                        "source_code": test_method_source_code,
                        "source_method_id": source_method_id
                    })

    return test_methods
    #
    # for _, class_node in tree.filter(javalang.tree.ClassDeclaration):
    #     for method in class_node.methods:
    #         if any(isinstance(anno, javalang.tree.Annotation) and anno.name == 'Test' for anno in method.annotations):
    #             method_details = parse_test_method_name(method.name)
    #             if method_details:
    #                 test_methods.append({
    #                     "test_method_name": method.name,
    #                     "details": method_details
    #                 })
    #
    # return test_methods


def create_test_json(directory, method_file_path):
    """
    Traverse the test directory and create a JSON file with test method details.
    Exclude files that contain '_scaffolding' in their names.
    """
    all_test_methods = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java") and "_scaffolding" not in file:
                file_path = os.path.join(root, file)
                print(f"at {file}")
                test_methods = process_test_file(file_path, method_file_path)
                print(f"processed {file}")
                all_test_methods.extend(test_methods)

    return json.dumps(all_test_methods, indent=4)


# Example usage
test_directory_path = "./dataset/2. Petclinic/Evosuite/"  # Replace with the actual path to the test directory
method_file_path = "./java_project_details_petclinic.json"
test_json = create_test_json(test_directory_path, method_file_path)

# Optionally, write to a file
output_file_path = "java_project_test_details_petclinic.json"
with open(output_file_path, "w") as output_file:
    output_file.write(test_json)
