import re

import pytest
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import ValidationError

from ice_breaker_v2 import KATEGORY_TEMPLATE
from parsers import ALLOWED_CATEGORIES, Category, CategoryNotFound, FinalResponse


def test_known_category_is_parsed_from_fenced_model_output():
    parser = PydanticOutputParser(pydantic_object=FinalResponse)
    model_output = (
        "Here is the result:\n"
        "```json\n"
        '{"final_output": {"predicted_category": "Tennis", "prediction_possibility": 0.95}}\n'
        "```"
    )

    result = parser.parse(model_output)

    assert isinstance(result.final_output, Category)
    assert result.final_output.predicted_category == "Tennis"
    assert result.final_output.prediction_possibility == pytest.approx(0.95)


def test_not_found_warning_is_parsed_and_unknown_category_is_rejected():
    warning = FinalResponse.model_validate(
        {"final_output": {"warning": "product category not found!"}}
    )
    assert isinstance(warning.final_output, CategoryNotFound)

    with pytest.raises(ValidationError):
        FinalResponse.model_validate(
            {"final_output": {"predicted_category": "Gardening", "prediction_possibility": 0.5}}
        )


def test_prompt_lists_exactly_the_allowed_categories():
    block = KATEGORY_TEMPLATE.split("Categories: [")[1].split("]")[0]
    listed = re.findall(r'"([^"]+)"', block)

    assert listed == ALLOWED_CATEGORIES


def test_category_validator_reports_the_rejected_value_and_missing_category():
    with pytest.raises(ValidationError, match="Invalid category: Gardening"):
        Category.model_validate({"predicted_category": "Gardening", "prediction_possibility": 0.5})

    with pytest.raises(ValidationError, match="Invalid category: None"):
        Category.model_validate({"prediction_possibility": 0.5})
