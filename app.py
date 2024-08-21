from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import get_questions_from_open_ai, get_questions_and_evaluations_from_open_ai
from uuid import uuid4

from firebase_admin import initialize_app, credentials, firestore

app = Flask(__name__)

CORS(app)

cred = credentials.Certificate("service_account_key.json")
_ = initialize_app(cred)
store = firestore.client()
doc_ref = store.collection(u'user_data')

def upload_feedback_to_firestore(session_id, feedback):
    data = { 'feedback': feedback }
    doc_ref.document(session_id).set(data, merge=True)

def upload_qa_to_firestore(session_id, difficulty, questions, answers):
    data = { str(difficulty): { 'questions': questions, 'answers': answers } }
    doc_ref.document(session_id).set(data, merge=True)

def upload_topic_to_firestore(session_id, topic):
    doc_ref.document(session_id).set({'topic': topic})

@app.get("/healthcheck")
def get_status():
    return "OK", 200

@app.post("/question")
def get_questions():

    payload = request.json
    payload_type = payload['type']

    if payload_type == 1:
        topic = payload['topic']
        data = get_questions_from_open_ai(topic)
        session_id = str(uuid4())
        response = {**data.model_dump(), 'sessionId': session_id}
        upload_topic_to_firestore(session_id, topic)

    elif payload_type == 2:
        topic = payload['topic']
        session_id = payload['sessionId']
        difficulty = payload['difficulty']
        questions = payload['questions']
        answers = payload['answers']
        submission = "\n".join([f"{question}\n{answer}" for question, answer in zip(questions, answers)])
        data = get_questions_and_evaluations_from_open_ai(topic, difficulty, submission)
        response = data.model_dump()
        upload_qa_to_firestore(session_id, difficulty, questions, answers)

    return jsonify(response)

@app.post("/log")
def log():

    payload = request.json
    session_id = payload['sessionId']
    feedback = payload['feedback']

    upload_feedback_to_firestore(session_id, feedback)

    return "uploaded", 201



    