"""
Example of how to use SafeOpenaiBackend class with OpenRouter API.

This example demonstrates how to configure the SafeOpenaiBackend class to send requests
to the OpenRouter server instead of the default OpenAI API.
"""

from rank_llm.rerank.listwise.rank_openai import SafeOpenaiBackend
from rank_llm.rerank.rankllm import PromptMode
from rank_llm.data import Request, Query, Candidate

import os

def create_openrouter_ranker():
    """
    Create a SafeOpenaiBackend instance configured for OpenRouter.
    
    Returns:
        SafeOpenaiBackend: Configured instance for OpenRouter API
    """
    
    # OpenRouter configuration
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    print("Using OpenRouter API key:", openrouter_api_key)

    openrouter_base_url = "https://openrouter.ai/api/v1"
    
    # Create SafeOpenaiBackend instance with OpenRouter configuration
    ranker = SafeOpenaiBackend(
        model="google/gemma-3-27b-it",  # Use OpenRouter model format (provider/model)
        context_size=8192,      # Model context size
        prompt_mode=PromptMode.RANK_GPT,  # Ranking prompt mode
        keys=[openrouter_api_key],        # Your OpenRouter API key(s)
        api_base=openrouter_base_url,     # OpenRouter API endpoint
        window_size=20,         # Window size for ranking
    )
    
    return ranker

def create_openrouter_ranker_minimal():
    """
    Create a minimal SafeOpenaiBackend instance for OpenRouter (without optional headers).
    
    Returns:
        SafeOpenaiBackend: Minimal configured instance for OpenRouter API
    """
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    print("Using OpenRouter API key:", openrouter_api_key)

    ranker = SafeOpenaiBackend(
        # model="openai/gpt-4o",
        model="google/gemma-3-27b-it",
        context_size=8192,
        keys=[openrouter_api_key],  # Replace with your actual key
        api_base="https://openrouter.ai/api/v1",
    )
    
    return ranker

def example_usage():
    """
    Example of how to use the OpenRouter-configured ranker.
    """
    
    # Create the ranker
    ranker = create_openrouter_ranker_minimal()
    
    requests = [
        Request(
            query=Query(text="What is the capital of France?", qid=1), 
            # quid="1",
            candidates=[
                Candidate(docid="doc1", doc={"text": "Berlin is the capital of Germany."},score=0.0),
                Candidate(docid="doc2", doc={"text": "Beijing is the capital of China."},score=0.0),
                Candidate(docid="doc3", doc={"text": "Paris is the capital of France."},score=0.0),
            ]
        )]
    results = ranker.rerank_batch(requests,populate_invocations_history=True,logging=True)
    print("Ranking results:")
    for result in results:
        print(f"Query: {result.query}")
        for candidate in result.candidates:
            print(f"  Candidate ID: {candidate.docid}, Score: {candidate.score}, Text: {candidate.doc}")
    
    print("OpenRouter ranker created successfully!")
    print(f"Model: {ranker.get_name()}")
    print(f"Using OpenRouter API at: {ranker.client.base_url}")

if __name__ == "__main__":
    example_usage()
