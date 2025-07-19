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
- [LangGraph quickstart](https://langchain-ai.github.io/langgraph/agents/agents/)
### OCI
- [Generative AI Service Inference API - Endpoints](https://docs.oracle.com/en-us/iaas/api/#/en/generative-ai-inference/20231130/)
- [Generative AI Service Management API - Endpoints](https://docs.oracle.com/en-us/iaas/api/#/en/generative-ai/20231130/)
- [GenerateText](https://docs.oracle.com/iaas/api/#/en/generative-ai-inference/20231130/GenerateTextResult/GenerateText)



- [Mensaje en slack](https://oracle-one.slack.com/archives/C05S3MBPRG8/p1719354535758469)

We’re happy to share that our latest integration is now available on LangChain.
This integration includes major updates with support for our latest models and features including: command-r/+, Llama 3, chat, and streaming.
To use you should be transitioning to the new chat interface ‘ChatOCIGenAI’ (vs ‘OCIGenAI’ still supported for legacy models).
To install use: pip install -qU langchain-community oci
And basic usage examples are available here
https://python.langchain.com/v0.2/docs/integrations/chat/oci_generative_ai/
and here
https://python.langchain.com/v0.2/docs/integrations/llms/oci_generative_ai/
For any questions feel free to contact Arthur (@archeng) and myself on this channel or directly.