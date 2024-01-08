import requests

API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
headers = {"Authorization": "Bearer hf_XXXXXX"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query({
    "inputs": "Write a python function that takes a string and reverses it.",
})
print(output)