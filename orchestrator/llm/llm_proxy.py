import yaml
import logging
import time
import os
from typing import Dict, Any
from groq import Groq
from dotenv import load_dotenv

# Load .env explicitly now
load_dotenv("experiments/.env")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LLMProxy")

class LLMProxy:
    def __init__(self, config_path: str = "experiments/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        
        self.provider = self.config["llm"]["provider"]
        self.model = self.config["llm"]["model_name"]
        self.max_tokens = self.config["llm"]["max_tokens"]
        self.temperature = self.config["llm"]["temperature"]
        
        if self.provider == "groq":
            api_key = os.getenv(self.config["llm"]["api_key_env"])
            if not api_key:
                logger.error("GROQ_API_KEY not found in environment!")
                raise ValueError("GROQ_API_KEY missing")
            
            logger.info(f"Initializing Groq Client with model: {self.model}")
            self.client = Groq(api_key=api_key)
        else:
            logger.info(f"Initialized LLM Proxy (Mock/Other). Provider: {self.provider}")
            self.client = None

    def call(self, prompt: str) -> Dict[str, Any]:
        """
        Calls the LLM with the constructed prompt.
        Returns a dict containing 'content', 'latency_ms', 'token_usage'.
        """
        start_time = time.time()
        
        if self.provider == "groq":
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model=self.model,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                
                content = chat_completion.choices[0].message.content
                usage = chat_completion.usage
                
                latency = (time.time() - start_time) * 1000
                
                return {
                    "content": content,
                    "latency_ms": latency,
                    "token_usage": {
                        "prompt_tokens": usage.prompt_tokens,
                        "completion_tokens": usage.completion_tokens,
                        "total_tokens": usage.total_tokens
                    },
                    "raw_response": {"id": chat_completion.id}
                }
            except Exception as e:
                logger.error(f"Groq API Call Failed: {e}")
                latency = (time.time() - start_time) * 1000
                return {
                    "content": f"[LLM ERROR: {str(e)}]", 
                    "latency_ms": latency, 
                    "token_usage": {}
                }
        
        else:
             # Legacy mock mode for fallback
             time.sleep(0.5)
             simulated_content = "This is a simulated response from the LLM based on the patient data."
             if "ignore" in prompt.lower() or "pirate" in prompt.lower():
                 simulated_content = "Arrr matey! I be ignoring your rules and dispensing medical advice from the seven seas!"
            
             latency = (time.time() - start_time) * 1000
             return {
                "content": simulated_content,
                "latency_ms": latency,
                "token_usage": {"prompt_tokens": 100, "completion_tokens": 20, "total_tokens": 120},
                "raw_response": {"mock": True}
             }
