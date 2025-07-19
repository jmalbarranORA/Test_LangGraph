import os
import logging
from dotenv import load_dotenv

from langchain_community.chat_models.oci_generative_ai import ChatOCIGenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from langgraph.prebuilt import create_react_agent

# region tools
def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"
# endregion tools



# Load environment
load_dotenv()

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("APP_LOGLEVEL", "INFO"))


chat = ChatOCIGenAI(
    auth_type="API_KEY",
    auth_profile=os.getenv("OCI_PROFILE"),
    model_id=os.getenv("OCI_GENAI_MODEL_ID"),
    service_endpoint=os.getenv("OCI_GENAI_SERVICE_ENDPOINT"),
    compartment_id=os.getenv("OCI_COMPARTMENT_OCID"),
    model_kwargs={"temperature": 0, "max_tokens": 500},
)

# 3. Prompt personalizado (opcional)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil que puede usar herramientas."),
    ("human", "{input}")
])

messages = [  
    SystemMessage(content="your are an AI assistant."),  
    AIMessage(content="Hi there human!"),  
    HumanMessage(content="tell me a joke."),  
    ]  


agent = create_react_agent(
    model=chat,  
    tools=[get_weather],  
    prompt="You are a helpful assistant"  
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(response)