from typing import TypedDict, List, Optional, Union, Any
import os
import logging
from dotenv import load_dotenv

from pydantic import BaseModel

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, AnyMessage, BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.checkpoint.memory import InMemorySaver




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


# region: LangGraph components
class SimpleStateGraph(TypedDict):
    messages: List[Union[BaseMessage, dict]]
    # add more fields if needed

class WeatherResponse(BaseModel):
    conditions: str


# endregion: LangGraph components

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

config: RunnableConfig = {"configurable": 
                            {"user_name": "John Smith",
                             "thread_id": "1"
                             } 
                        }
 

# checkpointer = InMemorySaver()


agent = create_react_agent(
    model=chat,
    tools=[get_weather],  
    response_format=WeatherResponse 
)

sf_messages = [  
    SystemMessage(content="You are an AI assistant."),  
    # AIMessage(content="Hi there human!"),  
    HumanMessage(content="What is the weather in sf?"),  
    ] 

# Run the agent
sf_response = agent.invoke({"messages": sf_messages}, config=config) # type: ignore

log_response(sf_response, logging.DEBUG)

# Print last message as response
print(sf_response["structured_response"])




# endregion: Process