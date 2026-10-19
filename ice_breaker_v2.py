"""Classify a product into a fixed category list with a local Ollama model.

The prompt asks the model for strict JSON, which is parsed into the Pydantic
models of ``parsers.py`` (an unknown category is rejected by the validator).
"""

import argparse

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from parsers import FinalResponse

DEFAULT_PRODUCT = "chair"

# Promt
KATEGORY_TEMPLATE = """
    You are an assistant tasked with classifying product information.

    Product: {product}

    Do NOT use any other category suggestion exept the "Categories" list below.
    Categories: [
        "Hunting",
        "Athletics",
        "Aikido",
        "Badminton",
        "Ballet",
        "Fishery",
        "Basketball",
        "Billiards",
        "Riding",
        "Bicycle",
        "Boxing",
        "Bushcraft",
        "Baseball",
        "Ice Hockey",
        "Ice Skating",
        "Bowling",
        "Dive",
        "Fitness",
        "Football",
        "Futsal",
        "Golf",
        "Wrestling",
        "Handball",
        "Hiking, Trekking, Outdoor",
        "Gymnastics and Trampoline",
        "Judo",
        "Camp",
        "Canoe and SUP",
        "Skiing, Snowboarding",
        "Running and Walking",
        "Karate",
        "Cricket",
        "Spade",
        "E-Sports",
        "Ping Pong",
        "Motorcycle",
        "Archery and Target Sports",
        "Orienteering",
        "Padel",
        "Skate, Skateboard, and Scooter",
        "Pickleball",
        "Pilates, Light Fitness Training",
        "Beach Tennis, Speedball",
        "Wind Sports",
        "Surfing",
        "Sporty Child and Physical Education",
        "Squash",
        "Tennis",
        "Climbing and Mountaineering",
        "Volleyball",
        "Windsurfing",
        "Sail",
        "Yoga",
        "Swimming"
    ]

    Find the products category above the list. If the product category is not found, return a warning message.

    Provide the result in strict JSON format as shown below and if the product category is not found, return a warning message:
    if the product category is found:
    {{
        "final_output": {{
            "predicted_category": "Category Name",
            "prediction_possibility": 0.95
        }}
    }}

    If the product category is not found:
    {{
        "final_output": {{
            "warning": "product category not found!"
        }}
    }}
    """


def build_chain(llm):
    """Prompt | model | Pydantic parser chain that expects a ``product`` input."""
    kategory_promt = PromptTemplate(
        input_variables=["product"], template=KATEGORY_TEMPLATE
    )
    parser = PydanticOutputParser(pydantic_object=FinalResponse)
    return kategory_promt | llm | parser


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Classify a product name into the fixed category list with a local Ollama model."
    )
    parser.add_argument(
        "product",
        nargs="?",
        default=DEFAULT_PRODUCT,
        help=f'product name or description (default: "{DEFAULT_PRODUCT}")',
    )
    args = parser.parse_args(argv)

    load_dotenv()

    # Model (needs a running Ollama server with the model pulled: ollama pull llama3.1:8b)
    # llm = ChatOpenAI(temperature=0.1, model_name="gpt-4o")  # alternative; needs langchain_openai
    llm = ChatOllama(model="llama3.1:8b")

    # Chain
    chain = build_chain(llm)

    # Run
    res = chain.invoke(input={"product": args.product})
    print(res)


if __name__ == "__main__":
    main()
