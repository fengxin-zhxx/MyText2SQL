from flask import Flask, render_template, request

from utils.db_utils import add_a_record

app = Flask(__name__)


@app.route("/")
def home():
    return index()

@app.route("/chatbot")
def index():
    return render_template("index.html")

@app.route("/get_db_ids")
def get_db_ids():
    return ["id1", "id2"]

@app.route("/get_db_ddl")
def get_db_ddl():
    db_id = request.args.get('db_id')
    return "db_id : " + db_id


@app.route("/flush")
def flush():
    print("Resetting Chatbot.")
    pass

@app.route("/get")
def get_bot_response():
    question = request.args.get('msg')
    db_id = request.args.get('db_id')
    # add_a_record(question, db_id)
    
    if question.strip() == "":
        return "Sorry, your question is empty."
    
    
    print("Question After ChatGPT: " + question)
    

    predicted_sql = "SELECT * FROM XXX"
    print("predicted sql:", predicted_sql)

    response = "<b>Database:</b><br>" + db_id + "<br><br>"
    response += "<b>Predicted SQL query:</b><br>" + predicted_sql
    return response

app.run(host = "0.0.0.0", debug = False)