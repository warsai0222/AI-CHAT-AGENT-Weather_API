import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
load_dotenv()  # fallback for when the script is launched from the project root

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WEATHER_STACK_API_KEY = os.getenv("WEATHER_STACK_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing. Add it to your .env file.")
if not WEATHER_STACK_API_KEY:
    raise ValueError("WEATHER_STACK_API_KEY is missing. Add it to your .env file.")

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    temperature=0,
    timeout=30,
)

search_tool = TavilySearchResults(
    max_results=2,
    api_wrapper=TavilySearchAPIWrapper(tavily_api_key=TAVILY_API_KEY),
)


@tool
def get_current_weather(location: str) -> str:
    """Get the current weather for a given location."""
    url = (
        f"https://api.weatherstack.com/current"
        f"?access_key={WEATHER_STACK_API_KEY}&query={location}"
    )
    response = requests.get(url)
    data = response.json()

    if "current" not in data:
        return (
            f"Could not retrieve weather data for {location}. "
            "Please check the location and try again."
        )

    temperature = data["current"]["temperature"]
    weather = data["current"]["weather_descriptions"][0]
    return (
        f"The current temperature in {location} is {temperature}°C "
        f"with {weather}."
    )


def build_agent():
    return create_react_agent(
        model=llm,
        tools=[search_tool, get_current_weather],
        debug=True,
    )


# Build ONCE
agent = build_agent()


def ask(question: str):
    result = agent.invoke({
        "messages": [("user", question)]
    })

    return result["messages"][-1].content
