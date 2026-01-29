from langchain.chat_models import init_chat_model
from agents.support.state import State
from agents.support.nodes.conversation.tools import tools
from agents.support.nodes.conversation.prompt import SYSTEM_PROMPT

llm = init_chat_model("openai:gpt-4o-mini", temperature=0)
llm = llm.bind_tools(tools)

def conversation(state: State):
    new_state = State()
    history = state.get("messages")
    customer_name = state.get("customer_name", "user")
    messages = [
        ("system", SYSTEM_PROMPT),
    ] + list(history)
    ai_message = llm.invoke(messages)
    new_state["messages"] = [ai_message]

    return new_state