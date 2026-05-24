from google import genai

from config.settings import settings
from llm.base import BaseLLM
from llm.models import LLMRequest, LLMResponse

class GeminiLLM(BaseLLM):
    
    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        
        self.model = settings.GEMINI_MODEL
        
    def generate(
        self, 
        request: LLMRequest
    ) -> LLMResponse:  

        prompt = f"""
        SYSTEM:
        {request.system_prompt}

        USER:
        {request.user_prompt}
        """.strip()
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": request.temperature
            }
        )
        
        if response.text is None:
            raise RuntimeError(
                "No response from Gemini API"
            )
    
        return LLMResponse(
            content=response.text,
            model=self.model
        )
    