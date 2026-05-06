# Configuration utilities for the meeting ticket extractor

import os
import dspy
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()

def configure_lm(provider="openai", model="gpt-3.5-turbo"):
    """Configure the language model for DSPy"""
    load_environment()
    
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        lm = dspy.LM(f"openai/{model}", api_key=api_key)
    elif provider == "mistral":
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables")
        # Mistral uses OpenAI-compatible API
        lm = dspy.LM(f"openai/{model}", api_key=api_key, api_base="https://api.mistral.ai/v1")
    elif provider == "mock":
        # For testing without actual LM calls
        # We'll use a simple configuration that doesn't require actual LM
        print("Using mock configuration for testing")
        return None
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    
    dspy.configure(lm=lm)
    print(f"Configured {provider} LM: {model}")
    return lm

def get_available_providers():
    """Return list of available LM providers"""
    return ["openai", "mistral", "mock"]

def test_configuration():
    """Test the configuration setup"""
    try:
        lm = configure_lm("mock")
        print("Configuration test successful!")
        return True
    except Exception as e:
        print(f"Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    test_configuration()