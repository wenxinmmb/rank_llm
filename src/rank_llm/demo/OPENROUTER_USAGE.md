# Using SafeOpenaiBackend with OpenRouter

This guide explains how to use the `SafeOpenaiBackend` class to send requests to OpenRouter instead of the default OpenAI API.

## What was changed

The `SafeOpenaiBackend` class has been created to support:

1. **OpenRouter API endpoint**: Uses the new OpenAI client with custom `base_url`
2. **OpenRouter-specific headers**: Supports optional `HTTP-Referer` and `X-Title` headers
3. **Model format**: Works with OpenRouter's model naming convention (e.g., `openai/gpt-4o`)
4. **Backward compatibility**: Still works with regular OpenAI and Azure AI configurations

## Key modifications

### 1. New parameter: `openrouter_config`
```python
openrouter_config: Optional[Dict[str, str]] = None
```

This optional parameter accepts a dictionary with:
- `site_url`: Your site URL for rankings on openrouter.ai (optional)
- `site_name`: Your site name for rankings on openrouter.ai (optional)

### 2. Enhanced client initialization
The class now creates an OpenAI client instance with proper configuration for custom endpoints.

### 3. OpenRouter headers support
When `openrouter_config` is provided, the class automatically adds the required headers to API requests.

## Usage Examples

### Basic OpenRouter Configuration

```python
from src.rank_llm.rerank.listwise.rank_openai import SafeOpenaiBackend

ranker = SafeOpenaiBackend(
    model="openai/gpt-4o",  # OpenRouter model format
    context_size=8192,
    keys=["your-openrouter-api-key"],
    api_base="https://openrouter.ai/api/v1"
)
```

### Full OpenRouter Configuration with Headers

```python
from src.rank_llm.rerank.listwise.rank_openai import SafeOpenaiBackend
from rank_llm.rerank.rankllm import PromptMode

openrouter_config = {
    "site_url": "https://yoursite.com",
    "site_name": "Your App Name"
}

ranker = SafeOpenaiBackend(
    model="openai/gpt-4o",
    context_size=8192,
    prompt_mode=PromptMode.RANK_GPT,
    keys=["your-openrouter-api-key"],
    api_base="https://openrouter.ai/api/v1",
    openrouter_config=openrouter_config,
    window_size=20
)
```

### Multiple API Keys (for load balancing)

```python
ranker = SafeOpenaiBackend(
    model="openai/gpt-4o",
    context_size=8192,
    keys=[
        "openrouter-key-1",
        "openrouter-key-2",
        "openrouter-key-3"
    ],
    api_base="https://openrouter.ai/api/v1"
)
```

## Available OpenRouter Models

You can use any model available on OpenRouter. Popular options include:

- `openai/gpt-4o`
- `openai/gpt-4o-mini`
- `openai/gpt-3.5-turbo`
- `anthropic/claude-3-sonnet`
- `anthropic/claude-3-haiku`
- `meta-llama/llama-3.1-70b-instruct`
- `google/gemini-pro`

## Environment Variables

You can also set your OpenRouter API key as an environment variable:

```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

Then use it in your code:
```python
import os

ranker = SafeOpenaiBackend(
    model="openai/gpt-4o",
    context_size=8192,
    keys=[os.getenv("OPENROUTER_API_KEY")],
    api_base="https://openrouter.ai/api/v1"
)
```

## Error Handling

The modified class maintains the same error handling and key cycling functionality:

- If a request fails, it automatically cycles to the next API key
- Rate limiting and quota management work the same way
- All existing error messages and retry logic are preserved

## Backward Compatibility

The modifications are fully backward compatible:

- **Regular OpenAI**: The original `SafeOpenai` class still works exactly as before
- **Azure OpenAI**: Still works with `api_type`, `api_base`, and `api_version` parameters
- **Existing code**: No changes needed for current implementations using `SafeOpenai`
- **OpenRouter**: Use the new `SafeOpenaiBackend` class for OpenRouter functionality

## Complete Working Example

```python
from src.rank_llm.rerank.listwise.rank_openai import SafeOpenaiBackend
from rank_llm.rerank.rankllm import PromptMode
from rank_llm.data import Request, Result

# Configure for OpenRouter
ranker = SafeOpenaiBackend(
    model="openai/gpt-4o",
    context_size=8192,
    prompt_mode=PromptMode.RANK_GPT,
    keys=["your-openrouter-api-key"],
    api_base="https://openrouter.ai/api/v1",
    openrouter_config={
        "site_url": "https://yoursite.com",
        "site_name": "Your App"
    }
)

# Use the ranker (assuming you have Request objects)
# requests = [Request(...), ...]
# results = ranker.rerank_batch(requests)
```

## Notes

1. **API Key Format**: Use your OpenRouter API key, not OpenAI keys
2. **Model Names**: Use OpenRouter's model naming format (provider/model)
3. **Rate Limits**: OpenRouter has its own rate limits, different from OpenAI
4. **Pricing**: Check OpenRouter's pricing page for model costs
5. **Headers**: The optional headers help with rankings on OpenRouter's leaderboard

## Getting Started with OpenRouter

1. Sign up at [openrouter.ai](https://openrouter.ai)
2. Get your API key from the dashboard
3. Replace `<OPENROUTER_API_KEY>` with your actual key
4. Choose a model from their available options
5. Start making requests!
