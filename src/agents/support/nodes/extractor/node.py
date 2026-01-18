from agents.support.state import State
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT

class ContactInfo(BaseModel):
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email of the person")
    tone: int = Field(description="The tone of the person", ge=0, le=100)
    age: int = Field(description="The age of the person")
    sentiment: str = Field(description="The sentiment of the person")

llm = init_chat_model("openai:gpt-4o-mini", temperature=0)
llm = llm.with_structured_output(ContactInfo)

def extractor(state: State):
    history = state.get("messages")
    customer_name = state.get("customer_name", None)
    customer_email = state.get("customer_email", None)
    new_state = State()
    if customer_name is None or customer_email is None:
        schema = llm.invoke([("system", SYSTEM_PROMPT) + history])
        if customer_name is None:
            new_state["customer_name"] = schema.name
        if customer_email is None:
            new_state["customer_email"] = schema.email
    return new_state