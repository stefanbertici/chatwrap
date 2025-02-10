# Description: Client for chatwrap
# Sends a request to the LLM server / api

import requests

class LlmClient:
    def __init__(self, url):
        self.url = url

        print(f"Connecting to {url}")

        response = requests.get(f'{self.url}/v1/models')
        if response.status_code == 200:
            print("Connected successfully")
            models = response.json()
            print(f"Available models: {models}")

    def generate(self, prompt, model, temperature, stream):
        response = requests.post(f'{self.url}/api/v0/completions', json={
            'prompt': prompt,
            'model': 'hermes-3-llama-3.2-3b' if model is None else model,
            'temperature': 0.7 if temperature is None else temperature,
            'stream': stream,
            'max_tokens': 50,
            "stop": '\n'
        })
        return response.json()