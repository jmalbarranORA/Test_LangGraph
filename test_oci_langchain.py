import os
import logging
from dotenv import load_dotenv

from langchain_community.chat_models.oci_generative_ai import ChatOCIGenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

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

messages = [  
    SystemMessage(content="your are an AI assistant."),  
    AIMessage(content="Hi there human!"),  
    HumanMessage(content="tell me a joke."),  
    ]  

response = chat.invoke(messages, temperature=0.7, max_tokens=500)

print(response)