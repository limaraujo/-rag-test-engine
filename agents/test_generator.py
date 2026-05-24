from llm.gemini import GeminiLLM
from llm.models import LLMRequest


class TestGeneratorAgent:

    def __init__(self):

        self.llm = GeminiLLM()

    def generate(
        self,
        input: str
    ) -> str:

        request = LLMRequest(
            system_prompt="""
            Você é um especialista em geração
            de testes unitários com pytest.
            """,

            user_prompt=input,

            temperature=0.1
        )

        response = self.llm.generate(
            request
        )

        return response.content