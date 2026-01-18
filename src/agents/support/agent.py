from langgraph.graph import StateGraph, START, END
from agents.support.nodes.extractor.node import extractor
from agents.support.nodes.conversation.node import conversation
from agents.support.state import State

builder = StateGraph(State)

builder.add_node('extractor', extractor)
builder.add_node('conversation', conversation)

builder.add_edge(START, 'extractor')
builder.add_edge('extractor', 'conversation')
builder.add_edge('conversation', END)

graph = builder.compile()