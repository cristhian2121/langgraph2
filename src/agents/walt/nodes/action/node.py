from langchain.agents import create_agent
from agents.walt.nodes.action.tools import tools
from agents.walt.nodes.action.prompt import prompt_template

action_node = create_agent(
    model="openai:gpt-4o-mini",
    tools=tools,
    system_prompt=prompt_template,
)
