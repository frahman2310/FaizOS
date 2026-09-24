# Fact sheet: prices, tokens, limits

**Fetched 2026-09-24** from the providers' official pages. Every unit that mentions a price or token rate
takes it from here, never from memory. Prices change: refresh this sheet before relying on it after
2026-12-31 (Gemini's listed prices change on 2027-01-01).

Sources:
- Anthropic: https://platform.claude.com/docs/en/about-claude/pricing (read in full)
- OpenAI: https://developers.openai.com/api/docs/pricing (read through a summarising fetch; spot-check before use)
- Google: https://ai.google.dev/gemini-api/docs/pricing (read through a summarising fetch; spot-check before use)

## Prices per million tokens (standard tier, USD)

| Provider | Model | Input | Cached input (read) | Output |
|---|---|---|---|---|
| Anthropic | Claude Fable 5.1 | 10.00 | 0.25 | 50.00 |
| Anthropic | Claude Opus 5.5 | 4.00 | 0.20 | 20.00 |
| Anthropic | Claude Opus 5 | 5.00 | 0.50 | 25.00 |
| Anthropic | Claude Sonnet 5 | 2.00 | 0.20 | 10.00 |
| Anthropic | Claude Sonnet 4.6 | 3.00 | 0.30 | 15.00 |
| Anthropic | Claude Haiku 4.5 | 1.00 | 0.10 | 5.00 |
| OpenAI | gpt-6-astra | 10.00 | 1.00 | 50.00 |
| OpenAI | gpt-6-sol | 2.00 | 0.20 | 10.00 |
| OpenAI | gpt-6-luna | 0.10 | 0.01 | 0.50 |
| OpenAI | gpt-5-mini | 0.25 | 0.025 | 2.00 |
| OpenAI | gpt-5-nano | 0.05 | 0.005 | 0.40 |
| Google | Gemini 3.5 Flash | 1.50 | 0.15 | 9.00 |
| Google | Gemini 3.5 Flash-Lite | 0.30 | n/a | 2.50 |
| Google | Gemini 3.8 Flash (price until 2026-12-31) | 0.75 | 0.075 | 3.75 |

Notes, Anthropic (quoted from the page):
- Sonnet 5's $2/$10 was introductory pricing and "is now the standard price"; the planned rise to $3/$15 "will not occur".
- Cache writes cost more than normal input: 1.25x base for a 5-minute cache, 2x for a 1-hour cache. Cache reads
  cost 0.1x base (0.05x on Opus 5.5, 0.025x on Fable 5.1). "Caching pays off after one cache read for the
  5-minute duration."
- Batch API: 50% off input and output, for all three providers.
- Claude 4.6 and later: the full 1M-token context window at standard pricing (a 900k-token request is billed
  at the same per-token rate as a 9k-token request).
- US-only inference (`inference_geo: "us"`): 1.1x on all token prices.

## Tokens

- Anthropic's rule of thumb: "1 token is approximately 4 characters or 0.75 words in English. The exact count
  varies by language and content type."
- **But** Claude 4.7 and later (including Sonnet 5, Opus 5 and 5.5) "use a newer tokenizer ... This tokenizer
  produces approximately 30% more tokens for the same text." Sonnet 4.6 and earlier use the older one. So the
  4-characters rule overstates characters per token for the newest Claude models.
- Claude's tokenizer is not public; exact Claude counts come from Anthropic's token-counting endpoint (needs an
  API key). The local demos count with two public tokenizers (OpenAI o200k and Qwen) to show the mechanism.
- Anthropic's page-size estimates for web fetch: a 10 kB web page is about 2,500 tokens; a 100 kB documentation
  page about 25,000; a 500 kB PDF about 125,000.
- Tool use adds a hidden system prompt, for example 354 tokens on Sonnet 5 and 286 on Opus 5 and 5.5, plus the tools' own
  definitions.

## Worked example from the source (Anthropic, Claude Managed Agents)

A one-hour session on Claude Opus 5 with 50,000 input and 15,000 output tokens: input $0.25, output $0.375,
runtime $0.08, total $0.705. With 40,000 of the input tokens read from cache: $0.525.
