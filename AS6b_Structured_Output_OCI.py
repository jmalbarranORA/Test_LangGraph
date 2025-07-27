from typing import TypedDict, List, Optional, Union, Any
import os
import logging


from dotenv import load_dotenv

from pydantic import BaseModel, ConfigDict

# from langchain_community.chat_models.oci_generative_ai import ChatOCIGenAI
from langchain_oci.chat_models.oci_generative_ai import ChatOCIGenAI
from langchain_core.tools import tool, StructuredTool
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
    model_config = ConfigDict(
        title="WeatherResponse",
        description="Weather conditions for a given city"
    )

# endregion: LangGraph components

# region: Agent tools

# @tool(description="Get weather for a given city.")
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
chat = ChatOCIGenAI(
    auth_type="API_KEY",
    auth_profile=os.getenv("OCI_PROFILE"),
    verbose=True,
    model_id=os.getenv("OCI_GENAI_MODEL_ID"),
    service_endpoint=os.getenv("OCI_GENAI_SERVICE_ENDPOINT"),
    compartment_id=os.getenv("OCI_COMPARTMENT_OCID"),
    model_kwargs={"temperature": 0, # Set temperature to 0 to get deterministic results
                  "max_tokens": 500},
)

config: RunnableConfig = {"configurable": 
                            {"user_name": "John Smith",
                             "thread_id": "1"
                             } 
                        }
 

# checkpointer = InMemorySaver()

get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    name="get_weather",
    description="Get weather for a given city.",)

agent = create_react_agent(
    model=chat,
    tools=[get_weather_tool],  
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