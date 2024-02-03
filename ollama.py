import requests
import json

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json'
}

constructed_prompt = ("Write a java functions that bumps the version formatted as XX.XX.XX a string where the two "
                      "right most XX can only go from 00 to 99 but the left most one can go on forever.")

data = {
    "model": "codellama:7b-instruct",
    "prompt": constructed_prompt,
    "stream": False,
    "keep_alive": "-1"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    response_text = response.text
    data = json.loads(response_text)
    actual_response = data["response"]
    print(actual_response)
else:
    print("Error:", response.status_code, response.text)