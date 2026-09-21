'''Chat completion against NanoGPT's OpenAI-compatible API.

Usage:
    NANOGPT_API_KEY=... NANOGPT_BASE_URL=... python examples/openai_compatible_chat.py 'your prompt'

NANOGPT_BASE_URL is the base URL from the API page in your NanoGPT account.
The model ID is the vendor/model form shown in the model directory.
NanoGPT states that every chat completion includes the exact cost charged;
the field name is not in the crawled pages, so this script prints any
non-standard top-level keys for you to find it.
'''
import json
import os
import sys

import requests

MODEL = 'anthropic/claude-opus-5'
STANDARD_KEYS = {'id', 'object', 'created', 'model', 'choices', 'usage', 'system_fingerprint'}


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('usage: openai_compatible_chat.py <prompt>')
    prompt = ' '.join(sys.argv[1:])

    base_url = os.environ['NANOGPT_BASE_URL'].rstrip('/')
    api_key = os.environ['NANOGPT_API_KEY']

    resp = requests.post(
        base_url + '/chat/completions',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json'},
        json={
            'model': MODEL,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 300,
        },
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()

    print('reply:', data['choices'][0]['message']['content'])
    print('usage:', json.dumps(data.get('usage'), indent=2))

    extra = {k: v for k, v in data.items() if k not in STANDARD_KEYS}
    print('extra fields (cost should be here):', json.dumps(extra, indent=2))


if __name__ == '__main__':
    main()
