import os
import javalang
import json
import hashlib

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


def extract_java_details(file_path):
    """
    Extracts details from a Java file: package name, class name, methods, and their Javadocs.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    tree = javalang.parse.parse(content)

    # Extracting the package name or using a default if not present
    package_name = tree.package.name if tree.package else "default_package"
    java_details = {
        "package_name": tree.package.name if tree.package else None,
        "classes": []
    }

    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        class_details = {
            "class_name": node.name,
            "methods": []
        }

        for method in node.methods:
            start_line, _ = method.position
            end_line = start_line  # Initialize end_line as start_line

            # Find the end line of the method
            if method.body:
                for statement in method.body:
                    if hasattr(statement, 'position') and statement.position:
                        end_line = max(end_line, statement.position.line)

            # Constructing the full method signature
            modifiers = ' '.join(sorted(method.modifiers))  # Sort and join modifiers
            params = ', '.join([f"{param.type.name} {param.name}" for param in method.parameters])
            method_signature = f"{modifiers} {method.return_type.name if method.return_type else 'void'} {method.name}({params})"

            # Create a unique ID
            param_types = '-'.join([param.type.name for param in method.parameters])
            unique_id_string = f"{package_name}::{node.name}::{method.name}::{param_types}"
            unique_id = hashlib.md5(unique_id_string.encode()).hexdigest()[:8]

            method_details = {
                "id": unique_id,
                "method_name": method.name,
                "signature": method_signature,
                "code": extract_lines_from_file(file_path, start_line - 1, end_line + 1),
                "javadoc": method.documentation
            }
            class_details["methods"].append(method_details)

        java_details["classes"].append(class_details)

    return java_details


def traverse_directory(directory):
    """
    Traverses the directory and processes each Java file.
    """
    java_files_details = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                java_details = extract_java_details(file_path)
                java_files_details.append(java_details)

    return java_files_details


# Example usage
directory_path = "./dataset/2. Petclinic/source-codes/main"  # Replace with the actual path to the Java project
java_project_details = traverse_directory(directory_path)

# Convert the extracted details to JSON
json_output = json.dumps(java_project_details, indent=4)

# Optionally, write to a file
with open("java_project_details_petclinic.json", "w") as output_file:
    output_file.write(json_output)
