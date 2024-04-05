from text2sql import ChatBot
from chatGPT.ChatAgent import chatAgent



from flask import Flask, render_template, request
from langdetect import detect
from utils.translate_utils import translate_zh_to_en
from utils.db_utils import add_a_record
from langdetect.lang_detect_exception import LangDetectException

chatAgent.reset()
text2sql_bot = ChatBot()
# replace None with your API token
baidu_api_token = None

app = Flask(__name__)


@app.route("/")
def home():
    return index()

@app.route("/chatbot")
def index():
    return render_template("index.html")

@app.route("/get_db_ids")
def get_db_ids():
    global text2sql_bot
    return text2sql_bot.db_ids

@app.route("/get_db_ddl")
def get_db_ddl():
    global text2sql_bot
    db_id = request.args.get('db_id')
    
    return text2sql_bot.db_id2ddl[db_id]


@app.route("/flush")
def flush():
    chatAgent.reset()

@app.route("/get")
def get_bot_response():
    global text2sql_bot
    question = request.args.get('msg')
    db_id = request.args.get('db_id')
    add_a_record(question, db_id)
    
    if question.strip() == "":
        return "Sorry, your question is empty."
    
    # TODO 使用ChatGPT完成翻译和多轮对话部分
    
    # 提问-回答-记录
    chatAgent.messages.append({"role": "user", "content": question})
    answer = chatAgent.ask_gpt()
    
    chatAgent.messages.append({"role": "assistant", "content": answer})

    question = answer
    
    print("Question After ChatGPT: " + question)
    

    predicted_sql = text2sql_bot.get_response(question, db_id)
    print("predicted sql:", predicted_sql)

    response = "<b>Database:</b><br>" + db_id + "<br><br>"
    response += "<b>Predicted SQL query:</b><br>" + predicted_sql
    return response

app.run(host = "0.0.0.0", debug = False)