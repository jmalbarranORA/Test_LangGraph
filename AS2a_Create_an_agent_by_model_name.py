from typing import Any
import os
import logging
from dotenv import load_dotenv

from langgraph.prebuilt import create_react_agent

# region: Common Utils
def log_response(response, loglevel: int = logging.INFO):
    if response is None:
        logger.error("No response from agent")
        raise ValueError("No response from agent")
    else:
        if response["messages"] is None:
            logger.error("No messages in response")
            raise ValueError("No messages in response")

    for message in response["messages"]:
        logger.log(level=loglevel, msg=f"{message.type}: {message.content}")
# endregion: Common Utils

# Load environment
load_dotenv()

# Initialize logging
logging.basicConfig(level=os.getenv("APP_LOGLEVEL", "INFO").upper(), format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    model="openai:o4-mini",  # Automatic model selection
    tools=[get_weather],  
    prompt="You are a helpful assistant"  
)

# Run the agent
response: dict[str, Any] | Any = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

log_response(response, logging.DEBUG)

# Print last message as response
print(response["messages"][-1].content)