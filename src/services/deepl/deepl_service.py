import requests


class DeeplService:
    def __init__(self, deepl_api_key: str):
        self.deepl_api_key = deepl_api_key

    def translate(self, text: str, source_language_code: str, target_language_code: str) -> str:

        url = 'https://api-free.deepl.com/v2/translate'
        params = {
            'auth_key': self.deepl_api_key,
            'text': text,
            'source_lang': source_language_code.upper(),
            'target_lang': target_language_code.upper(),
        }

        response = requests.post(url, data=params)
        response_data = response.json()

        if response.status_code != 200 or 'translations' not in response_data:
            raise Exception(f'Error in translation: {response_data}')

        return response_data['translations'][0]['text']
