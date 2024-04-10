import openai
import json
import os

with open('chatGPT/settings.json', 'r', encoding='utf-8') as f:
    settings = json.loads(f.read())
    
base_url=settings['base_url']
api_key=settings['api_key']
model=settings['model']


with open('chatGPT/prompt.json', 'r', encoding='utf-8') as f:
    prompt = json.loads(f.read())['prompt']


client = openai.OpenAI(
    base_url=base_url,
    api_key=api_key
)

class ChatGPT:
    def __init__(self, prompt=prompt, model="gpt-3.5-turbo"):
        self.messages = [{"role": "system", "content": prompt}]
        self.model= model
        
    def reset(self):
        self.messages = [{"role": "system", "content": prompt}]
        self.model= model

    def ask_gpt(self):
        chat_completion = client.chat.completions.create(
            messages=self.messages,
            model=self.model,
        )
        return chat_completion.choices[0].message.content