from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import get_questions_from_open_ai, get_questions_and_evaluations_from_open_ai

import time

app = Flask(__name__)

CORS(app)


def get_questions_1(topic):

    return { 
        "questions": [{
            "subtopic": "stupidity",
            "question": "what the fuck?"
        }]*10
    }

def get_questions_2(topic, submission):

    return {
        "questions": [{
            "subtopic": "stupidity",
            "question": "what the fuck?"
        }]*10,
        "evaluations": [{
            "status": "correct",
	        "explanation": "you're stupid",
	        "reason_if_wrong": "it is not"
        }]*10
    }

@app.post("/questions")
def get_questions():

    payload = request.json
    payload_type = payload['type']

    if payload_type == 1:
        topic = payload['topic']
        data = get_questions_from_open_ai(topic)
    elif payload_type == 2:
        topic = payload['topic']
        difficulty = 2
        questions = payload['questions']
        answers = payload['answers']
        submission = "\n".join([f"{question}\n{answer}" for question, answer in zip(questions, answers)])
        data = get_questions_and_evaluations_from_open_ai(topic, difficulty, submission)
    
    # return data
    
    print(data.model_dump_json())

    return jsonify(data.model_dump())
    