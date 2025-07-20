# Configure Development environmet

- Install pyenv
    - Mac: `brew install pyenv`
- Edit file `sample.env` and parameters. Rename file to .env
    - For installation, `OCI_PROFILE` environment parameter matching file ~/.oci/config
- Execute `source configureEnvironment.sh`. This script
    - Install version python 3.12 if not installed yet and set it as current local version (file `.python-version`)
    - Create environment for installing required packages. Use capability .nosync for avoiding problems with OneDrive (this trick only works in Mac so if you use OneDrive try another no-sync solution)
    - Activate environment
    - Install requirements.txt
- Get API keys and save in `.env` file
    - [Anthropic](https://console.anthropic.com/settings/keys)


# LangGraph tutorial
## Links
### LangChain/LangGraph
- [LangChain:Oracle Cloud Infrastructure Generative AI](https://python.langchain.com/docs/integrations/llms/oci_generative_ai/#oracle-cloud-infrastructure-generative-ai)
- [LangChain Providers: Oracle Cloud Infrastructure (OCI)](https://python.langchain.com/docs/integrations/providers/oci/)
    - [Class: ChatOCIModelDeployment](https://python.langchain.com/api_reference/community/chat_models/langchain_community.chat_models.oci_data_science.ChatOCIModelDeployment.html#chatocimodeldeployment)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [LangGraph: Quickstart](https://langchain-ai.github.io/langgraph/agents/agents/)
### OCI
- [Generative AI Service Inference API - Endpoints](https://docs.oracle.com/en-us/iaas/api/#/en/generative-ai-inference/20231130/)
- [Generative AI Service Management API - Endpoints](https://docs.oracle.com/en-us/iaas/api/#/en/generative-ai/20231130/)
- [GenerateText](https://docs.oracle.com/iaas/api/#/en/generative-ai-inference/20231130/GenerateTextResult/GenerateText)


## Tutorial
### Quick start
#### Start with a prebuilt agent
2. Create an agent
- Changed the original code for creating the model using `ChatOCIGenAI`. As it's a community model, cannot be loaded directly from LangGraph by name
3. Configure an LLM
- Already done in previous step
4. Add a custom prompt
- New concept [AgentState](https://medium.com/@gitmaxd/understanding-state-in-langgraph-a-comprehensive-guide-191462220997)
- New concept [Context](https://langchain-ai.github.io/langgraph/agents/context/)
    - Config: Run parameters (non mutable )
    - Short-term memory: Data changing during conversation
    - Long-term memory: Data shared between conversations
5. Add memory
    - **NOTICE**: LangGraph's checkpointer (even InMemorySaver) uses msgpack under the hood to serialize the state between steps. msgpack can only handle native Python types (like dicts, lists, strings, etc.), and LangChain's AIMessage is not serializable by default. So we require changes in code (again, thanks ChatGPT!)
        - Create a agent_safe Runnable from agent, serializing and deserializing the BaseMessage element
    



# PENDING
## Notes for frontend  (Thank you, ChatGPT!)


✅ 1. LangServe (Recomendado)
🟢 Mejor opción si usas LangGraph y quieres un API + front básico tipo Streamlit.

Es un servidor FastAPI listo para producción.

Se integra directo con LangGraph y Runnable.

Puedes obtener:

/invoke, /stream, /openapi.json, etc.

Un mini frontend incluido (básico pero útil).

Puedes combinarlo con herramientas como Chainlit, Gradio, o incluso Next.js si quieres UI más pro.

Ejemplo básico
```bash
pip install langserve
```
```python
# app.py
from langserve import add_routes
from langgraph.graph import StateGraph
from fastapi import FastAPI
from your_langgraph_build import build_graph  # tu grafo LangGraph como Runnable

app = FastAPI()
graph_runnable = build_graph()
add_routes(app, graph_runnable, path="/graph")
```
```bash
uvicorn app:app --reload
```
Visita http://localhost:8000/graph/playground para un frontend estilo OpenAI Playground.

✅ 2. Chainlit (Front tipo Streamlit, especializado en LLMs)
🟢 Ideal si quieres una interfaz de chat sofisticada con 0 configuración.

Similar a Streamlit, pero orientado a chatbots con agentes, tools, LangChain, LangGraph.

Compatible con Runnable.

```bash
pip install chainlit
```

```python

# chainlit_app.py
import chainlit as cl
from your_langgraph_build import build_graph

graph_runnable = build_graph()

@cl.on_message
async def on_message(message: cl.Message):
    result = graph_runnable.invoke({"input": message.content})
    await cl.Message(content=str(result)).send()
```
```bash
chainlit run chainlit_app.py
```
Interfaz de chat moderna, soporte para herramientas, memoria, streaming, etc.

✅ 3. Gradio (rápido + muy visual)
🟡 Más visual e intuitivo si quieres sliders, imágenes, audio, etc.

```bash

pip install gradio
```

```python
import gradio as gr
from your_langgraph_build import build_graph

graph_runnable = build_graph()

def chat_fn(message):
    result = graph_runnable.invoke({"input": message})
    return str(result)

gr.ChatInterface(chat_fn).launch()

```
✅ 4. Next.js + LangServe (para frontend serio)
🔵 Profesional, ideal para apps web serias.

Usa LangServe como backend.

Puedes consumir /invoke desde Next.js o React.

Muy flexible, pero más trabajo que Chainlit o Gradio.

📌 Comparativa rápida
Opción	Facilidad	UI Tipo Chat	Producción	Personalización
LangServe	🟢 Alta	❌ Básico	✅ Sí	🟡 Media
Chainlit	🟢 Alta	✅ Sí	✅ Sí	🟢 Alta
Gradio	🟢 Alta	✅ Sí	🟡 Parcial	🟢 Alta
Next.js	🔴 Baja	✅ (via React)	✅ Sí	🟢 Muy alta

👉 Recomendación
Para algo tipo Streamlit, pero optimizado para LangGraph:

✅ Usa Chainlit si quieres UI rápida tipo chat.
✅ Usa LangServe si quieres API + frontend REST sin esfuerzo.
🟡 Usa Gradio si quieres combinar con elementos visuales.

