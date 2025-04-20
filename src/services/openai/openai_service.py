import os
from typing import Dict, List
import requests


class OpenAIService:
    
    def __init__(self, openai_key, model: str = 'gpt-4o-mini'):

        
        self.api_key = openai_key
        if not self.api_key:
            raise ValueError('Chave de API da OpenAI não definida no .env.')

        self.api_base_url = 'https://api.openai.com/v1/chat/completions'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        self.model = model


    def _make_api_call(self, messages: List[Dict[str, str]]) -> str:
        payload = {
            'model': self.model,
            'messages': messages,
            'temperature': 0.3,
            'max_tokens': 4000,
        }

        try:
            response = requests.post(self.api_base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()

        except requests.exceptions.RequestException as e:
            error_message = f'Erro na chamada de API: {str(e)}'
            if hasattr(e, 'response') and e.response:
                error_message = f'{error_message} - {e.response.text}'
            raise Exception(error_message)


    def gpt_chat_completion(self, content: str, system_prompt: str) -> str:
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': content}
        ]
        
        return self._make_api_call(messages)
