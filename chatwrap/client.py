# Description: Client for chatwrap
# Sends a request to the LLM server / api

import json
from typing import Callable, Optional
from logger import log_calls
import requests

class LlmClient:
    def __init__(self, url):
        self.url = url

    @log_calls
    def get_models(self):
        response = requests.get(f'{self.url}/v1/models')
        return [item['id'] for item in response.json().get('data')] 

    def generate(self, prompt, model, temperature, max_tokens, stream, callback: Optional[Callable] = None):
        params = {
            'prompt': 'tell me a joke' if prompt in [None, ''] else prompt,
            'model': 'hermes-3-llama-3.2-3b' if model in [None, ''] else model,
            'temperature': 0.7 if temperature is None else temperature,
            'stream': False if stream is None else stream,
            'max_tokens': 250 if max_tokens is None else max_tokens,
            "stop": '\n'
        }

        if stream and callback:
            return self._handle_streaming_response(params, callback)
        else: 
            return self._handle_response(params)

    @log_calls
    def _handle_response(self, params):
        response = requests.post(f'{self.url}/api/v0/completions', json=params)
        return response.json().get('choices')[0].get('text')

    @log_calls
    def _handle_streaming_response(self, params, callback):
        full_response = []
        params['stream'] = True
        
        with requests.post(f'{self.url}/api/v0/completions', json=params, stream=True) as response:
            print('--------------------------------------')

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8').strip()

                    # Remove 'data: ' prefix if present
                    if decoded_line.startswith("data: "):
                        decoded_line = decoded_line[len("data: "):]

                    # Ignore '[DONE]' message
                    if decoded_line == "[DONE]":
                        continue

                    try:
                        chunk = json.loads(decoded_line)  # Parse the JSON
                        if chunk.get('choices'):
                            token = chunk['choices'][0].get('text', '')
                            full_response.append(token)
                            callback(token)  # Stream the token
                    except json.JSONDecodeError:
                        print(f"Warning: Failed to parse JSON: {decoded_line}")  # Debugging

        print('\n--------------------------------------')
        # Return the complete response text
        return ''.join(full_response)