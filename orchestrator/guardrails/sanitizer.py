import re
import logging
import yaml

logger = logging.getLogger("Guardrails-Sanitizer")

class Sanitizer:
    def __init__(self, config_path: str = "experiments/config.yaml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        self.enabled = config["guardrails"]["regex_scrubber"]["enabled"]
        
        # Regex patterns to scrub (PHI, internal IPs, etc.)
        self.patterns = [
            (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]"),
            (r"\b(192\.168\.\d{1,3}\.\d{1,3})\b", "[REDACTED_IP]")
        ]

    def process(self, text: str) -> str:
        if not self.enabled:
            return text
            
        cleaned_text = text
        for pattern, replacement in self.patterns:
            cleaned_text = re.sub(pattern, replacement, cleaned_text)
            
        if cleaned_text != text:
             logger.info("Sanitizer triggered: Redacted sensitive info.")
             
        return cleaned_text
