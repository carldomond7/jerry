from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from groq import Groq

groq_api_key = os.getenv("GROQ_API_KEY")

class UserRequest(BaseModel):
    query: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "plswork!"}

@app.post("/route/")
async def process_request(request: UserRequest):
    client = Groq()

    query = request.query

    # Use the query directly as the content of the user message in chat.completions.create()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Please carefully analyze the following request and create an enhanced prompt that addresses the key elements while providing additional context and instructions to optimize the output of a large language model (LLM). Consider the subject matter and intent of the original request, and preface your revised prompt with a relevant expert persona that the LLM should embody when responding. Aim to make the prompt clear, specific, and well-structured to elicit a high-quality and coherent response from the LLM."
            },
            {
                "role": "user",
                "content": query,
            }
        ],
        model="mixtral-8x7b-32768",
        temperature=0.5,
        max_tokens=32768,
        top_p=1,
        stop=None,
        stream=False,
    )

    # Return the completion returned by the Groq LLM
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    uvicorn.run(app)
