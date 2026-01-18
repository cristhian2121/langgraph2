from langchain.agents import create_agent
from agents.support.nodes.weather.tools import get_city_cordinates, check_weather
from agents.support.nodes.weather.prompt import prompt

weather_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_city_cordinates, check_weather],
    system_prompt=prompt,
    name="WeatherAgent",
)