import openai
import json
import os

from chatGPT.ChatGPT import ChatGPT

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

chatAgent = ChatGPT()

