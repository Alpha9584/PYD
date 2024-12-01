import os
from pathlib import Path
from threading import Lock
from anthropic import Anthropic

class AnthropicClient:
    _instance = None
    _lock = Lock()
    _client = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        if not self._client:
            project_root = Path(__file__).parent.parent
            api_key = os.getenv('API_KEY')
            
            if not api_key:
                raise ValueError("API_KEY environment variable not set")
                
            self._client = Anthropic(api_key=api_key)

    def get_client(self):
        return self._client

anthropic = AnthropicClient()
client = anthropic.get_client()