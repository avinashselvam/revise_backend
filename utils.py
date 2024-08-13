from typing import List
from pydantic import BaseModel
from openai import OpenAI
from enum import Enum

client = OpenAI()

MODEL = "gpt-4o-mini"

class Status(str, Enum):
	correct = "correct"
	unattempted = "unattempted"
	wrong = "wrong"

class Question(BaseModel):
	subtopic: str
	question: str

class Evaluation(BaseModel):
	status: Status
	explanation: str
	reason_if_wrong: str
	
class TypeOneResponse(BaseModel):
	questions: List[Question]

class TypeTwoResponse(BaseModel):
	evaluations: List[Evaluation]
	questions: List[Question]

def get_questions_from_open_ai(topic):

    prompt = f"I want to revise {topic} at increasing levels of difficulty from 1 to 4. Ask me 5 varied questions (mention the subtopic) from the topic with difficulty level 1 to get started. response should be in json format."

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        response_format=TypeOneResponse
    )

    output = completion.choices[0].message.parsed
	
    return output

def get_questions_and_evaluations_from_open_ai(topic, difficulty, submission):
	
    prompt = f"You're currently helping me revise {topic} at increasing levels of difficulty from 1 to 4. Below are the previous 10 questions that you asked me and my answers for them {submission}. Evaluate them. If correct, no explanation needed. If wrong, provide reason_if_wrong. If unattempted, provide answer in explanation. And then ask me 10 more questions from the same topic but with increased difficulty level of {difficulty}. response should be in json format."
	
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        response_format=TypeTwoResponse
    )

    output = completion.choices[0].message.parsed
	
    return output

### DUMMY DATA UTILS

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


