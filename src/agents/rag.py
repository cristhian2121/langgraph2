from langgraph.graph import MessagesState
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
import random

llm = init_chat_model("openai:gpt-4o-mini", temperature=0)

file_search_model = {
    "type": "file_search",
    "vector_store_ids": ["file_search_vector_store"]
}

#llm = llm.bind_tools([file_search_model])

class State(MessagesState):
    customer_name: str
    customer_email: str
    customer_phone: str
    customer_age: int

class ContactInfo(BaseModel):
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email of the person")
    phone: str = Field(description="The phone number of the person")
    tone: int = Field(description="The tone of the person", ge=0, le=100)
    age: int = Field(description="The age of the person")
    sentiment: str = Field(description="The sentiment of the person")

llm_with_structured_output = llm.with_structured_output(ContactInfo)

def extractor(state: State):
    history = state.get("messages")
    customer_name = state.get("customer_name", None)
    customer_email = state.get("customer_email", None)
    customer_phone = state.get("customer_phone", None)
    customer_age = state.get("customer_age", None)
    new_state = State()
    if customer_name is None or customer_name is None or customer_phone is None or customer_age is None:
        schema = llm_with_structured_output.invoke(history)
        new_state["customer_name"] = schema.name
        new_state["customer_email"] = schema.email
        new_state["customer_phone"] = schema.phone
        new_state["customer_age"] = schema.age
    return new_state

def conversation(state: State):
    new_state = State()
    history = state.get("messages")
    last_message = history[-1]
    customer_name = state.get("customer_name", "user")
    system_prompt = f"""
    You are a helpful assistant that can answer questions and help with tasks.
    You are given a conversation between a customer name {customer_name} and a support agent.
    You are also given the conversation history.
    """
    messages = [
        ("system", system_prompt),
        ("user", last_message.text)
    ]
    ai_message = llm.invoke(messages)
    new_state["messages"] = [ai_message]

    return new_state

from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)

builder.add_node('extractor', extractor)
builder.add_node('conversation', conversation)

builder.add_edge(START, 'extractor')
builder.add_edge('extractor', 'conversation')
builder.add_edge('conversation', END)

graph = builder.compile()