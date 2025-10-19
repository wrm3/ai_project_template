"""
Perplexity API integration tool.
Only use this when other methods have proven inadequate, as it has token usage costs.
"""
import os
import json
from typing import Optional, Dict, Any
import requests
from dotenv import load_dotenv

load_dotenv()

PERP_API_KEY = os.getenv("PERP_API_KEY")
PERP_BASE_URL = "https://api.perplexity.ai/chat/completions"

class PerplexityAPI:
    def __init__(self):
        if not PERP_API_KEY:
            raise ValueError("Perplexity API key not found in environment variables")
        
        self.headers = {
            "Authorization": f"Bearer {PERP_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Cost tracking (per 1K tokens)
        self.cost_per_1k = {
            "sonar-medium-online": 0.0025,  # $0.0025 per 1K tokens
            "sonar-medium-context": 0.0025,  # $0.0025 per 1K tokens
            "mixtral-8x7b-instruct": 0.0007,  # $0.0007 per 1K tokens
            "codellama-34b-instruct": 0.0007,  # $0.0007 per 1K tokens
        }

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation."""
        return len(text.split()) * 1.3  # Rough estimate: words * 1.3

    def estimate_cost(self, model: str, input_text: str) -> float:
        """Estimate cost for the API call."""
        estimated_tokens = self.estimate_tokens(input_text)
        cost_per_1k = self.cost_per_1k.get(model, 0.0025)  # Default to highest cost
        return (estimated_tokens / 1000) * cost_per_1k

    def query(
        self,
        prompt: str,
        model: str = "sonar-medium-online",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        require_confirmation: bool = True
    ) -> Dict[str, Any]:
        """
        Query the Perplexity API with cost estimation and confirmation.
        
        Args:
            prompt: The input text/question
            model: Model to use (sonar-medium-online, mixtral-8x7b-instruct, etc.)
            temperature: Randomness of the output (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            require_confirmation: Whether to require user confirmation before proceeding
            
        Returns:
            Dict containing the response and metadata
        """
        estimated_cost = self.estimate_cost(model, prompt)
        
        print(f"\nPerplexity API Call Details:")
        print(f"Model: {model}")
        print(f"Estimated cost: ${estimated_cost:.4f}")
        
        if require_confirmation:
            confirm = input("\nProceed with API call? (y/n): ").lower()
            if confirm != 'y':
                return {"error": "API call cancelled by user"}

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(PERP_BASE_URL, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Add metadata to response
            result["metadata"] = {
                "estimated_cost": estimated_cost,
                "model_used": model,
                "timestamp": response.headers.get("Date")
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {"error": f"API call failed: {str(e)}"}

    def research_query(
        self,
        question: str,
        require_sources: bool = True,
        max_tokens: int = 2048
    ) -> Dict[str, Any]:
        """
        Specialized method for research queries that require source citations.
        Uses the online model for real-time information.
        """
        model = "sonar-medium-online"
        
        # Enhance prompt to require sources if needed
        if require_sources:
            prompt = f"""Please research the following question and provide a detailed answer with citations and sources:
            
Question: {question}

Please format your response with:
1. A clear, direct answer
2. Supporting details and context
3. Citations for all factual claims
4. Links to primary sources where available"""
        else:
            prompt = question

        return self.query(
            prompt=prompt,
            model=model,
            temperature=0.3,  # Lower temperature for more factual responses
            max_tokens=max_tokens
        )

def main():
    """Test the Perplexity API integration."""
    api = PerplexityAPI()
    
    # Test basic query
    response = api.query(
        "What are the latest developments in quantum computing?",
        require_confirmation=True
    )
    
    print("\nAPI Response:")
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main() 