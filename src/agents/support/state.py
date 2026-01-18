from langgraph.graph import MessagesState

class State(MessagesState):
    customer_name: str
    customer_email: str
    customer_phone: str
    customer_age: int

