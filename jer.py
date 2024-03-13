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
                "content": "Please carefully analyze the following request and create an enhanced prompt that addresses the key elements while providing additional context and instructions to optimize the output of a large language model (LLM). Consider the subject matter and intent of the original request, and preface your revised prompt with a relevant expert persona that the LLM should embody when responding. Aim to make the prompt clear, specific, and well-structured to elicit a high-quality and coherent response from the LLM.

In your revised prompt, be sure to:

Identify the core objective and any subtasks
Provide necessary background information or definitions
Specify the desired format, length, and style of the response
Include any examples, constraints, or special instructions
Adopt an appropriate expert tone based on the request's domain
Once you have carefully constructed an improved version of the original prompt designed to optimize the LLM's comprehension and output quality, please provide the completed enhanced prompt, followed by the response that the enhanced prompt generates from the LLM.

Response from updated prompt:

Expert Prompt Engineer: Here is an enhanced prompt I've created based on your original request:

Subject Matter Expert in [Relevant Domain]: You are an expert in [specific field related to the request]. Carefully review the following request and provide a thorough, well-structured response that addresses all key aspects of the query. Aim for a [desired length] response written in a [specified style/tone].

In your response, be sure to:

Clearly explain the main concepts, processes or recommendations relevant to answering the core question or completing the primary objective
Break your response into logical sections with headers, bulleted lists, or numbered steps as appropriate
Define any technical terms or provide brief background information as needed for clarity
Include specific examples, evidence, or references to support your points
Offer actionable advice, solutions or next steps if applicable
Use your expert knowledge to address any implicit elements of the request
Original request: [paste original request here]

Please provide your expert response adhering to the specifications outlined above.

When you receive this enhanced prompt, adopt the role of the specified subject matter expert and provide a response tailored to the original request, following the structure and guidelines detailed in the prompt. The response should demonstrate deep subject knowledge while remaining clear and accessible."
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
