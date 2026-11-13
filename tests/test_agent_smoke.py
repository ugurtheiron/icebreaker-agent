from langchain_core.prompts import PromptTemplate

from agents import linkedin_lookup_agent as agent
from tools import tools

# Same variables and ReAct format as the "hwchase17/react" prompt on LangChain Hub.
REACT_PROMPT = PromptTemplate.from_template(
    "Answer the following questions as best you can. You have access to the following tools:\n\n"
    "{tools}\n\n"
    "Use the following format:\n\n"
    "Question: the input question you must answer\n"
    "Thought: you should always think about what to do\n"
    "Action: the action to take, should be one of [{tool_names}]\n"
    "Action Input: the input to the action\n"
    "Observation: the result of the action\n"
    "Thought: I now know the final answer\n"
    "Final Answer: the final answer to the original input question\n\n"
    "Begin!\n\n"
    "Question: {input}\n"
    "Thought:{agent_scratchpad}"
)
PROFILE_URL = "https://www.linkedin.com/in/jane-doe-example/"
SEARCH_RESULT = f"[{{'url': '{PROFILE_URL}', 'content': 'Jane Doe - Software Engineer'}}]"


def test_lookup_runs_the_react_loop_and_returns_the_final_answer_url(monkeypatch, fake_llm):
    llm, prompts = fake_llm(
        "Thought: I need to search for the profile page.\n"
        "Action: Crawl Google 4 linkedin profile page\n"
        "Action Input: Jane Doe",
        f"Thought: I now know the final answer\nFinal Answer: {PROFILE_URL}",
    )
    pulled, searched = [], []
    monkeypatch.setattr(agent.hub, "pull", lambda repo: pulled.append(repo) or REACT_PROMPT)
    monkeypatch.setattr(agent, "ChatOpenAI", lambda **kwargs: llm)
    monkeypatch.setattr(
        agent, "get_profile_url_tavily", lambda name: searched.append(name) or SEARCH_RESULT
    )

    url = agent.lookup(name="Jane Doe")

    assert url == PROFILE_URL
    assert pulled == ["hwchase17/react"]
    assert searched == ["Jane Doe"]  # the model's Action Input reached the tool
    assert len(prompts) == 2  # one model call per ReAct step
    assert "Jane Doe" in prompts[0]
    assert f"Observation: {SEARCH_RESULT}" in prompts[1]  # tool output is fed back to the model


def test_command_line_entry_point_prints_the_looked_up_url(monkeypatch, capsys):
    monkeypatch.setattr(agent, "lookup", lambda name: f"{PROFILE_URL}?q={name}")

    agent.main(["Jane Doe"])

    assert capsys.readouterr().out.strip() == f"{PROFILE_URL}?q=Jane Doe"


def test_tavily_helper_searches_for_the_name_and_returns_the_result(monkeypatch):
    queries = []

    class FakeTavily:
        def run(self, query):
            queries.append(query)
            return SEARCH_RESULT

    monkeypatch.setattr(tools, "TavilySearchResults", FakeTavily)

    assert tools.get_profile_url_tavily("Jane Doe") == SEARCH_RESULT
    assert queries == ["Jane Doe"]
