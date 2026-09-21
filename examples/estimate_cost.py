'''Estimate NanoGPT cost from a usage dict using the published list prices.

No network. Prices are per 1M tokens and copied from one snapshot of
nano-gpt.com (pricing page and text model directory); refresh them before
relying on the numbers. NanoGPT bills at list price with no markup; the two
opt-in surcharges on the pricing page are modelled with flags:
  pinned_provider  manually pinning a specific provider adds 5%
  byok             bring-your-own-key requests are billed 5% of normal cost
'''

PRICES = {
    # model id: (input, output, cache_read, cache_write_5m, cache_write_1h)
    'openai/gpt-5.5': (5.00, 30.00, None, None, None),
    'anthropic/claude-opus-5': (5.00, 25.00, 0.50, 6.25, 10.00),
}


def estimate(model, usage, pinned_provider=False, byok=False, cache_write_1h=False):
    inp, out, cache_read, cw5, cw1 = PRICES[model]
    per = 1_000_000
    cost = usage.get('prompt_tokens', 0) * inp / per
    cost += usage.get('completion_tokens', 0) * out / per
    cached = usage.get('cached_tokens', 0)
    if cached and cache_read is not None:
        # cached tokens are billed at the cache-read rate instead of input
        cost += cached * (cache_read - inp) / per
    written = usage.get('cache_write_tokens', 0)
    if written:
        rate = cw1 if cache_write_1h else cw5
        if rate is None:
            raise ValueError(f'{model}: no cache write price in the table')
        cost += written * rate / per
    if pinned_provider:
        cost *= 1.05
    if byok:
        cost *= 0.05
    return round(cost, 6)


if __name__ == '__main__':
    sample = {'prompt_tokens': 1200, 'completion_tokens': 400, 'cached_tokens': 800}
    for model in PRICES:
        base = estimate(model, sample)
        print(f'{model:28s} list {base:.6f}  pinned {estimate(model, sample, pinned_provider=True):.6f}  byok {estimate(model, sample, byok=True):.6f}')
