[GitHub issue: Original](https://github.com/langchain-ai/langchain/issues/32122)
[GitHub issue: Redirected LangChain Community](https://github.com/langchain-ai/langchain-community/issues/182))

[Pull Request y Tests](https://chatgpt.com/share/687fce65-00b8-8011-a517-d2457f29d236)
[Contribute Integrations    ](https://python.langchain.com/docs/contributing/how_to/integrations/)

[Custom Chat Models](https://python.langchain.com/docs/how_to/custom_chat_model/)

The file that needs to be amended is site-packages/langchain_community/chat_models/oci_generative_ai.py

I created this helper function at the beginning of the code:

```
def make_json_safe(value: Any) -> Any:
        """Recursively convert value to a JSON-serializable format."""
        if isinstance(value, dict):
            return {k: make_json_safe(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [make_json_safe(v) for v in value]
        elif hasattr(value, "__dict__"):
            return make_json_safe(vars(value))
        elif hasattr(value, "_asdict"):  # for namedtuples
            return make_json_safe(value._asdict())
        elif isinstance(value, (str, int, float, bool)) or value is None:
            return value
        else:
            return str(value)  # fallback: convert to string
```
And modified the chat_generation_info function for Cohere Provider as follows:

```
    def chat_generation_info(self, response: Any) -> Dict[str, Any]:
        chat_response = response.data.chat_response

        generation_info: Dict[str, Any] = {
            "documents": make_json_safe(chat_response.documents),
            "citations": make_json_safe(chat_response.citations),
            "search_queries": make_json_safe(chat_response.search_queries),
            "is_search_required": chat_response.is_search_required,
            "finish_reason": chat_response.finish_reason,
        }

        if getattr(chat_response, "tool_calls", None):
            generation_info["tool_calls"] = make_json_safe(
                _format_oci_tool_calls(chat_response.tool_calls)
            )

        return generation_info
```


# Comentario en slack

We were initially contributing to the LangChain repo, but the LangChain maintainers have stopped accepting new feature request PRs.
They suggested we maintain our own separate repo for same.
As a result, we've created a new repository:  https://github.com/oracle/langchain-oracle.
We've recently received approvals for this, and while the work is still in progress, our goal is to release the package to PyPI soon.
In the meantime, please use the langchain-community package. We will make an official announcement once the new package is available.
For more details, please refer to this documentation: OCI Generative AI Integration.
Please note that, at this time, the package supports only Meta and Cohere models.