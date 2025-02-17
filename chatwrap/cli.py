# Description: Command line interface for chatwrap

from argparse import ArgumentParser
from chatwrap.streaming_callback import StreamingCallback
from chatwrap.client import LlmClient

LLM_SERVER_URL = 'http://127.0.0.1:1234'

def main(params):
    client = LlmClient(LLM_SERVER_URL, 'llama-3.2-3b-instruct')

    models = client.get_models()
    print(f'~ Hello, welcome to Chatwrap! These are the currently available models for use:{models}')

    model = input('~ Please select a [model] from the list above or leave blank for default: ')
    prompt = input('~ Please enter a [prompt] or leave blank for default: ')
    
    callback = StreamingCallback() if params.stream is True else None
    answer = client.generate(prompt, model, params.temperature, params.max_tokens, params.stream, callback)
    print(f'~ LLM generated answer: {answer}')

if __name__ == '__main__':
    args = ArgumentParser('Chatwrap')
    args.add_argument('--temperature', help='Temperature to use')
    args.add_argument('--max_tokens', help='Maximum number of tokens to use')
    args.add_argument('--stream', action='store_true', help='Stream the output')
    params = args.parse_args()
    main(params);