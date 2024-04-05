import openai
import json
import os

from chatGPT.ChatGPT import ChatGPT

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

chatAgent = ChatGPT()

def main():
    
    # 循环
    while 1:
        # 提问
        q = input(f"【你】")
  
        # 提问-回答-记录
        chatAgent.messages.append({"role": "user", "content": q})
        answer = chatAgent.ask_gpt()
        
        print(f"【ChatGPT】{answer}")
        chatAgent.messages.append({"role": "assistant", "content": answer})

if __name__ == '__main__':
    main()
