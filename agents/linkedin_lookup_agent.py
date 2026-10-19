"""ReAct agent that looks up a person's LinkedIn profile URL with a Tavily search tool.

Derived from agents/linkedin_lookup_agent.py of Eden Marco's LangChain course
(https://github.com/emarco177/langchain-course, Apache-2.0, see NOTICE).
Changed by Uğur Özdemir: prompt wording, imports from langchain_core, and a
command-line entry point that takes the name to look up.
"""

import argparse
import os
import sys

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from tools.tools import get_profile_url_tavily  # noqa: E402

load_dotenv()


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    template = """given the full name {name_of_person} of a person I want you to get it me a link to their LinkedIn profile page.
                Your answer should contain only an URL"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

    react_promt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_promt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    linkedin_url = result["output"]
    return linkedin_url


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Find the LinkedIn profile URL of a person with a ReAct agent and Tavily search."
    )
    parser.add_argument("name", help='full name to look up, e.g. "Jane Doe"')
    args = parser.parse_args(argv)
    print(lookup(name=args.name))


if __name__ == "__main__":
    main()
