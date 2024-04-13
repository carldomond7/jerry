from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from langchain.chains import LLMChain  # Update with the correct import based on your langchain package
from langchain.prompts import PromptTemplate  # Update with the correct import based on your langchain package
from langchain_groq import ChatGroq  # Update with the correct import based on your langchain package


groq_api_key = os.getenv("GROQ_API_KEY")


class UserRequest(BaseModel):
    query: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "plswork!"}




@app.post("/route/")
async def process_request(request: UserRequest):
    llm = ChatGroq(
        groq_api_key=groq_api_key, 
        model_name='mixtral-8x7b-32768',
        streaming=True)


    query = request.query

    prompt_template = """
    Clearly explain the main concepts, processes or recommendations relevant to answering the core question or completing the primary objective
    Break your response into logical sections with headers, bulleted lists, or numbered steps as appropriate
    Define any technical terms or provide brief background information as needed for clarity
    Include specific examples, evidence, or references to support your points
    Offer actionable advice, solutions or next steps if applicable
    Use your expert knowledge to address any implicit elements of the request
    Original QUERY: {query}

    Please provide your expert response adhering to the specifications outlined above.

    When you receive this enhanced prompt, adopt the role of the specified subject matter expert and provide a response tailored to the original request, following the structure and guidelines detailed in the prompt. The response should demonstrate deep subject knowledge while remaining clear and accessible. BE SURE TO PROVIDE SOLELY THE ANSWER DO NOT PROVIDE STATE THAT YOU REVISED THE PROMPT!
    """


# Define the prompt structure
    prompt = PromptTemplate(
    input_variables=["query"],
    template=prompt_template,
)




    llm_chain = LLMChain(llm=llm, prompt=prompt)


    # Pass the context and question to the Langchain chain
    result_chain = llm_chain.ainvoke({"query": query})


    return result_chain


if __name__ == "__main__":
        uvicorn.run(app)
