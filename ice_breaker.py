"""Turn a LinkedIn profile into a short summary and two interesting facts.

Derived from the "Ice Breaker" project of Eden Marco's LangChain course
(https://github.com/emarco177/langchain-course, Apache-2.0, see NOTICE).
Changed by Uğur Özdemir: command-line arguments, profile loading from a bundled
synthetic sample, and the chain wrapped in a function so it can be tested.
"""

import argparse

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile

SUMMARY_TEMPLATE = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary of the person
    2. two interesting facts about them
    """


def build_chain(llm):
    """Prompt | model chain that expects an ``information`` input."""
    prompt = PromptTemplate(input_variables=["information"], template=SUMMARY_TEMPLATE)
    return prompt | llm


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Summarise a LinkedIn profile and list two interesting facts about the person."
    )
    parser.add_argument(
        "--url",
        help="LinkedIn profile URL to fetch through the Proxycurl API (needs PROXYCURL_API_KEY).",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="use the bundled synthetic sample profile instead of calling Proxycurl.",
    )
    return parser


def main(argv=None) -> None:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    if not args.mock and not args.url:
        parser.error("pass --url <profile url>, or --mock to use the bundled sample profile")

    load_dotenv()

    # Model
    llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")

    # Chain
    chain = build_chain(llm)

    linkedin_data = scrape_linkedin_profile(args.url, mock=args.mock)

    # Run
    res = chain.invoke(input={"information": linkedin_data})
    print(res.content)


if __name__ == "__main__":
    main()
