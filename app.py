from text2sql import ChatBot
from chatGPT.ChatAgent import chatAgent


from flask import Flask, render_template, request, jsonify
from utils.translate_utils import translate_zh_to_en
from utils.db_utils import add_a_record, update_db, execute_sql_with_pretty_table, get_cursor_from_path
import os
from urllib import parse


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
    # add_a_record(question, db_id)
    
    if question.strip() == "":
        return "Sorry, your question is empty."
    

    chatAgent.add_question(question)
    
    answer = chatAgent.ask_gpt()
    
    print("ChatGPT Reply:", answer)

    question = answer.split("Answer_En: ")[1]
    
    print("Question After ChatGPT: " + question)
    

    predicted_sql = text2sql_bot.get_response(question, db_id)
    print("predicted sql:", predicted_sql)

    response = {"Database" : db_id}
    response["Question after llm"] = question
    response["Predicted SQL query"] = predicted_sql
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


@app.route('/run', methods=['GET'])
def run_SQL():
    db = request.args.get('db')
    SQL = parse.unquote(request.args.get('sql'))
    
    print(db, SQL)
    db_path = os.path.join("databases", db, db + ".sqlite")
    return execute_sql_with_pretty_table(get_cursor_from_path(db_path), SQL)


app.run(host = "0.0.0.0", debug = False)