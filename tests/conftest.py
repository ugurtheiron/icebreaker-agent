import os

# Keep the suite offline even when the shell or a local .env turns LangSmith
# tracing on. The modules under test call load_dotenv() on import, and
# load_dotenv() does not override variables that are already set, so pinning
# them here (before anything from LangChain is imported) wins over both.
for _name in (
    "LANGCHAIN_TRACING_V2",
    "LANGSMITH_TRACING_V2",
    "LANGCHAIN_TRACING",
    "LANGSMITH_TRACING",
):
    os.environ[_name] = "false"

import pytest  # noqa: E402
from langchain_core.callbacks import BaseCallbackHandler  # noqa: E402
from langchain_core.language_models.fake_chat_models import FakeListChatModel  # noqa: E402


class _PromptRecorder(BaseCallbackHandler):
    """Collects the text of every prompt a chat model receives."""

    def __init__(self, prompts):
        self.prompts = prompts

    def on_chat_model_start(self, serialized, messages, **kwargs):
        self.prompts.extend("\n".join(str(m.content) for m in batch) for batch in messages)


@pytest.fixture
def fake_llm():
    """Factory for a scripted chat model: ``llm, prompts = fake_llm("reply 1", "reply 2")``.

    The model answers with the given replies in order and appends the text of
    every prompt it was called with to ``prompts``. No network, no API key.
    """

    def make(*replies):
        prompts = []
        llm = FakeListChatModel(responses=list(replies), callbacks=[_PromptRecorder(prompts)])
        return llm, prompts

    return make
