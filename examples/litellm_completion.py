'''The same NanoGPT chat call through the LiteLLM SDK.

LiteLLM documents NanoGPT as a provider (docs.litellm.ai/docs/providers/nano-gpt),
so the call below has the same shape as a call to OpenAI, Anthropic or any
other LiteLLM provider. Set NANOGPT_LITELLM_MODEL to the model string that
provider page shows; the fallback below is illustrative only.
'''
import os
import sys

import litellm

# Illustrative fallback - copy the real prefix from the LiteLLM provider page.
DEFAULT_MODEL = 'nano-gpt/anthropic/claude-opus-5'


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('usage: litellm_completion.py <prompt>')
    prompt = ' '.join(sys.argv[1:])

    model = os.environ.get('NANOGPT_LITELLM_MODEL', DEFAULT_MODEL)
    api_key = os.environ['NANOGPT_API_KEY']
    # Only needed if the provider page tells you to pass a base URL explicitly.
    api_base = os.environ.get('NANOGPT_BASE_URL')

    kwargs = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 300,
        'api_key': api_key,
    }
    if api_base:
        kwargs['api_base'] = api_base

    response = litellm.completion(**kwargs)

    print('reply:', response.choices[0].message.content)
    print('usage:', response.usage)


if __name__ == '__main__':
    main()
