from text2sql import ChatBot
from chatGPT.ChatAgent import chatAgent


from flask import Flask, render_template, request, jsonify
from utils.translate_utils import translate_zh_to_en
from utils.db_utils import add_a_record, update_db
import os

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


@app.route("/flush", methods=['post'])
def flush():
    chatAgent.reset()
    return "chatagent refreshed."

@app.route("/get")
def get_bot_response():
    global text2sql_bot
    question = request.args.get('msg')
    db_id = request.args.get('db_id')
    add_a_record(question, db_id)
    
    if question.strip() == "":
        return "Sorry, your question is empty."
    
    # 提问-回答-记录
    chatAgent.messages.append({"role": "user", "content": question})
    answer = chatAgent.ask_gpt()
    
    chatAgent.messages.append({"role": "assistant", "content": answer})

    question = answer
    
    print("Question After ChatGPT: " + question)
    

    predicted_sql = text2sql_bot.get_response(question, db_id)
    print("predicted sql:", predicted_sql)

    response = "<b>Database:</b><br>" + db_id + "<br><br>"
    response += "<b>Question after llm:</b><br>" + question + "<br>"
    response += "<b>Predicted SQL query:</b><br>" + predicted_sql
    return response




@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': '未选择文件'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': '未选择文件'}), 400

    file.save(os.path.join('uploads', file.filename))
    update_db(file.filename[:-7])
    # TODO： 刷新chatbot db列表
    global text2sql_bot
    text2sql_bot.reset()
    return jsonify({'message': file.filename + '上传成功'}), 200


app.run(host = "0.0.0.0", debug = False)