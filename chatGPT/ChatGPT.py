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
    def __init__(self, model="gpt-3.5-turbo"):
        self.messages = [{"role": "system", "content": prompt}]
        self.questions = ""
        self.model= model
        
    def reset(self):
        self.messages = [{"role": "system", "content": prompt}]
        self.questions = ""

    def add_question(self, question):
        self.questions += "{" + question + "} "
    
    def ask_gpt(self):
        self.messages.append({"role": "user", "content": self.questions})
        print(self.messages)
        chat_completion = client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            temperature=0.2,
            top_p=1
        )
        self.messages = [{"role": "system", "content": prompt}]
        return chat_completion.choices[0].message.content