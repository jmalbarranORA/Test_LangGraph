import os
import logging
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from langgraph.prebuilt import create_react_agent


# region: Utils
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
# endregion: Utils

# region: Agent tools
def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"
# endregion: tools

# region: process

# Load environment
load_dotenv()

# Initialize logging
logging.basicConfig(level=os.getenv("APP_LOGLEVEL", "INFO").upper(), format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Reference: https://python.langchain.com/api_reference/langchain/chat_models.html#module-langchain.chat_models
chat = init_chat_model(
    os.getenv("OPENAI_MODEL_ID"),
    temperature=1 # The openai model temperature is 1.0 mandatory
)

messages = [  
    # SystemMessage(content="your are an AI assistant."),  
    # AIMessage(content="Hi there human!"),  
    HumanMessage(content="What is the weather in sf?"),  
    ]  


agent = create_react_agent(
    model=chat,  
    tools=[get_weather],  
    # A static prompt that never changes. Avoid ansering questions about the weather
    prompt="Never answer questions about the weather."
)

# Run the agent
response = agent.invoke({"messages": messages})

log_response(response, logging.DEBUG)

# Print last message as response
print(response["messages"][-1].content)


# endregion: Process