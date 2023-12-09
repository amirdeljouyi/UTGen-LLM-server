import json

import requests


def load_json_data(file_path):
    """
    Load JSON data from a given file path.

    :param file_path: Path to the JSON file.
    :return: The data contained in the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


prompt_object = load_json_data('./prompts_with_details_petclinic.json')

counter = 1

for obj in prompt_object:
    API_URL = "http://localhost:11434/api/generate"
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "model": "codellama",
        "prompt": obj["prompt"],
        "stream": False
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        obj["response"] = data["response"]
    else:
        obj["response"] = "Error:" + response.status_code + response.text

    print(f"Finished run {counter} out of {len(prompt_object)}")
    counter += 1

output_file_path = "prompts_with_responses.json"

with open(output_file_path, "w") as output_file:
    output_file.write(prompt_object)
