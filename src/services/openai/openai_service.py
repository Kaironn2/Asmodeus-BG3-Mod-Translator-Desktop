


class OpenAIService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_response(self, prompt: str) -> str:
        # Placeholder for actual OpenAI API call
        return "This is a mock response based on the prompt: " + prompt
