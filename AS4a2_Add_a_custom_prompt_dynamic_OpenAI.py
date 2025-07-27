import os
import logging
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, AnyMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate

from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState



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

def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    """
    Returns a list of AnyMessage objects containing a system message with the username,
    and the user's messages. The username is taken from the configurable parameter
    if it exists, or the default value of "John Doe" is used.

    Args:
        state (AgentState): The current state of the agent.
        config (RunnableConfig): The configuration of the agent.

    Returns:
        list[AnyMessage]: A list of AnyMessage objects.
    """
    user_name = "John Doe"
    configurable = config.get("configurable")
    if configurable:
        user_name = configurable.get("user_name") or user_name
    system_msg = f"Address the user as {user_name}."
    return [SystemMessage(content=system_msg)] + state["messages"] # type: ignore


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

config: RunnableConfig = {"configurable": {"user_name": "John Smith"}}

messages = [  
    # SystemMessage(content="your are an AI assistant."),  
    # AIMessage(content="Hi there human!"),  
    HumanMessage(content="What is the weather in sf?"),  
    ]  


# Parameter: prompt
# An optional prompt for the LLM. Can take a few different forms:

#         - str: This is converted to a SystemMessage and added to the beginning of the list of messages in state["messages"].
#         - SystemMessage: this is added to the beginning of the list of messages in state["messages"].
#         - Callable: This function should take in full graph state and the output is then passed to the language model.
#         - Runnable: This runnable should take in full graph state and the output is then passed to the language model.


agent = create_react_agent(
    model=chat,  
    tools=[get_weather],  
    prompt=prompt # type: ignore

)

# Run the agent
response = agent.invoke(input={"messages": messages}, config=config)

log_response(response, logging.DEBUG)

# Print last message as response
print(response["messages"][-1].content)


# endregion: Process