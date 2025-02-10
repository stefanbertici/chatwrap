# Description: Command line interface for chatwrap

from argparse import ArgumentParser
from client import LlmClient

LLM_SERVER_URL = 'http://127.0.0.1:1234'

def main(params):
    client = LlmClient(LLM_SERVER_URL)
    print(client.generate(params.prompt, params.model, params.temperature, params.stream).get('choices')[0].get('text'))

if __name__ == '__main__':
    args = ArgumentParser('Chatwrap')
    args.add_argument('prompt', help='Prompt to use') 
    args.add_argument('--model', help='Command to use')
    args.add_argument('--temperature', help='Temperature to use')
    args.add_argument('--stream', action='store_true', help='Stream the output')
    params = args.parse_args()
    main(params);