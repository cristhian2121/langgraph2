from agents.support.state import State
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT

class ContactInfo(BaseModel):
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email of the person")
    phone: str = Field(description="The phone number of the person", default=None)
    tone: int = Field(description="The tone of the person", ge=0, le=100)
    age: int = Field(description="The age of the person")
    sentiment: str = Field(description="The sentiment of the person")

llm = init_chat_model("openai:gpt-4o-mini", temperature=0)
llm = llm.with_structured_output(ContactInfo)

def extractor(state: State):
    history = state.get("messages")
    customer_name = state.get("customer_name", None)
    customer_email = state.get("customer_email", None)
    customer_phone = state.get("customer_phone", None)
    customer_age = state.get("customer_age", None)
    new_state = State()
    if customer_name is None or customer_email is None or customer_phone is None or customer_age is None:
        messages = [("system", SYSTEM_PROMPT)] + list(history)
        schema = llm.invoke(messages)
        if customer_name is None:
            new_state["customer_name"] = schema.name
        if customer_email is None:
            new_state["customer_email"] = schema.email
        if customer_phone is None and schema.phone:
            new_state["customer_phone"] = schema.phone
        if customer_age is None:
            new_state["customer_age"] = schema.age
    return new_state