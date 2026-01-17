import logging
import yaml

logger = logging.getLogger("Guardrails-MedicalValidator")

class MedicalValidator:
    def __init__(self, config_path: str = "experiments/config.yaml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        self.enabled = config["guardrails"]["medical_consistency"]["enabled"]
        
        # Simple keywords that indicate dangerous medical advice in this toy setup
        self.forbidden_keywords = [
            "ignore previous medical history",
            "prescribe all drugs",
            "drink bleach",
            "fentanyl",
            "oxycodone",
            "xanax",
            "lethal dose"
        ]

    def validate(self, text: str) -> dict:
        """
        Returns {'valid': bool, 'reason': str}
        """
        if not self.enabled:
            return {"valid": True, "reason": "Disabled"}
            
        for keyword in self.forbidden_keywords:
            if keyword in text.lower():
                logger.warning(f"Medical Validator Blocked: {keyword}")
                return {"valid": False, "reason": f"Contains forbidden term: {keyword}"}
                
        return {"valid": True, "reason": "Passed static check"}
