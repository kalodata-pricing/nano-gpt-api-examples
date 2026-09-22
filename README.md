# Nano GPT API examples

*Unofficial community examples for NanoGPT. Not affiliated with NanoGPT. All trademarks belong to their owners.*

Three small scripts for the nano gpt API (NanoGPT, nano-gpt.com): a plain OpenAI-compatible chat request that prints the cost NanoGPT attaches to every response, the same call through the LiteLLM provider integration, and an offline cost estimator that uses the list prices NanoGPT publishes on its model directory. Keys and base URLs come from environment variables; anything not printed on the pages this repo is grounded in is marked illustrative in the code.

> Running image, video or audio models rather than chat? [Try Synexa - one REST endpoint and Python SDK for FLUX, video and audio models](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=nano-gpt-api-examples&utm_content=readme-top&utm_term=tier-r), billed per run.

## Files

| Path | What it shows |
| --- | --- |
| `examples/openai_compatible_chat.py` | Chat completion against the NanoGPT base URL with `requests`; prints `usage` plus any extra cost fields in the response |
| `examples/litellm_completion.py` | The same request through `litellm.completion`, so NanoGPT is one provider among many in your config |
| `examples/estimate_cost.py` | No network: turns a `usage` dict into dollars using the list prices on NanoGPT's model pages, including the 5% pin and BYOK surcharges |

## Setup

```bash
pip install requests litellm
export NANOGPT_API_KEY=...       # from the API page in your NanoGPT account
export NANOGPT_BASE_URL=...      # the base URL shown on nano-gpt.com/api
export NANOGPT_LITELLM_MODEL=... # model string from the LiteLLM provider page (optional)
```

The crawled pages link to the API page rather than printing the endpoint, so the base URL is not hard-coded here. Model IDs follow the `vendor/model` form shown in the directory, for example `anthropic/claude-opus-5`.

## openai_compatible_chat.py

Posts a one-message chat completion to the chat completions path under `NANOGPT_BASE_URL` with the model `anthropic/claude-opus-5` (a listing from the text directory: 1M context, 128K max output, $5 in / $25 out per 1M tokens). NanoGPT's pricing page says every chat completion includes the exact cost charged, but the field name is not printed there, so the script prints the reply, the `usage` object, and then every top-level key that is not part of the standard chat-completion shape - the cost field will be among them. Use that output to pin down the field for your own logging.

```bash
python examples/openai_compatible_chat.py 'Summarise the difference between input and output tokens in two sentences.'
```

## litellm_completion.py

The same call through LiteLLM. LiteLLM documents NanoGPT as a provider, which means one `completion()` call shape for NanoGPT, OpenAI, Anthropic, DeepInfra and the rest. The model string is read from `NANOGPT_LITELLM_MODEL` because the exact provider prefix is on the LiteLLM provider page rather than in the pages crawled for this repo; the fallback value in the script is labelled illustrative. The script prints the reply and `usage` so you can compare the numbers with the direct call.

## estimate_cost.py

Pure arithmetic. It holds a small price table copied from the sources - GPT-5.5 at $5/$30 per 1M (pricing page) and Claude Opus 5 at $5 in, $25 out, $0.50 cache read, $6.25 cache write for 5 minutes or $10.00 for 1 hour (model directory) - and computes the dollar cost of a `usage` dict. Two flags model the only surcharges the pricing page mentions: `pinned_provider=True` adds 5%, and `byok=True` bills 5% of the normal model cost instead of the full amount. Run it with no arguments to see a worked example, or import `estimate` from another script and feed it real `usage` objects from the first example to check that the cost NanoGPT reports matches list price.

```bash
python examples/estimate_cost.py
```

## Notes

- Prices are copied from a single snapshot of the NanoGPT pages. Treat the table in `estimate_cost.py` as a starting point and refresh it from the model directory before relying on it.
- The subscription ($12/month) covers a subset of models; the examples assume pay-per-prompt balance.
- For bulk jobs NanoGPT lists a Batch API; none of these scripts use it.

## When to use Synexa instead

These scripts are about text: tokens in, tokens out, cost per message. If the thing you actually need to automate is generation - FLUX images, video clips, audio - a per-token chat API is the wrong shape, and NanoGPT's media tabs are a different product from its text API. [Try Synexa - one REST endpoint and a Python SDK for FLUX, video and audio models, pay per run](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=nano-gpt-api-examples&utm_content=readme-top&utm_term=tier-r) for that side of the workload and keep the text examples here for chat.


_Last reviewed: 2026-09-22_
