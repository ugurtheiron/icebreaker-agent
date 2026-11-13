import pytest
from langchain_core.exceptions import OutputParserException

import ice_breaker
import ice_breaker_v2
from parsers import Category, CategoryNotFound
from third_parties.linkedin import scrape_linkedin_profile

SUMMARY = "Jane Doe is a software engineer.\nFact 1: she writes tests.\nFact 2: she likes tennis."


def test_summary_chain_puts_the_profile_in_the_prompt_and_returns_the_reply(fake_llm):
    llm, prompts = fake_llm(SUMMARY)
    profile = scrape_linkedin_profile(mock=True)

    reply = ice_breaker.build_chain(llm).invoke({"information": profile})

    assert reply.content == SUMMARY
    assert len(prompts) == 1
    assert "Jane Doe" in prompts[0]  # the profile data was interpolated
    assert "two interesting facts" in prompts[0]


def test_ice_breaker_main_prints_the_summary_in_mock_mode(monkeypatch, capsys, fake_llm):
    llm, prompts = fake_llm(SUMMARY)
    monkeypatch.setattr(ice_breaker, "ChatOpenAI", lambda **kwargs: llm)

    ice_breaker.main(["--mock"])

    assert capsys.readouterr().out.strip() == SUMMARY
    assert "Jane Doe" in prompts[0]


def test_category_chain_returns_the_parsed_category(fake_llm):
    llm, prompts = fake_llm(
        '```json\n{"final_output": {"predicted_category": "Tennis", "prediction_possibility": 0.9}}\n```'
    )

    result = ice_breaker_v2.build_chain(llm).invoke({"product": "tennis racket"})

    assert isinstance(result.final_output, Category)
    assert result.final_output.predicted_category == "Tennis"
    assert result.final_output.prediction_possibility == pytest.approx(0.9)
    assert "Product: tennis racket" in prompts[0]


def test_category_chain_returns_the_not_found_warning(fake_llm):
    llm, _ = fake_llm('{"final_output": {"warning": "product category not found!"}}')

    result = ice_breaker_v2.build_chain(llm).invoke({"product": "spoon"})

    assert isinstance(result.final_output, CategoryNotFound)
    assert result.final_output.warning == "product category not found!"


def test_category_chain_rejects_a_category_outside_the_list(fake_llm):
    llm, _ = fake_llm(
        '{"final_output": {"predicted_category": "Gardening", "prediction_possibility": 0.5}}'
    )

    with pytest.raises(OutputParserException, match="Invalid category: Gardening"):
        ice_breaker_v2.build_chain(llm).invoke({"product": "shovel"})


def test_ice_breaker_v2_main_prints_the_parsed_result(monkeypatch, capsys, fake_llm):
    llm, prompts = fake_llm(
        '{"final_output": {"predicted_category": "Yoga", "prediction_possibility": 0.8}}'
    )
    models = []
    monkeypatch.setattr(ice_breaker_v2, "ChatOllama", lambda **kwargs: models.append(kwargs) or llm)

    ice_breaker_v2.main(["yoga mat"])

    assert "predicted_category='Yoga'" in capsys.readouterr().out
    assert "Product: yoga mat" in prompts[0]
    assert models == [{"model": "llama3.1:8b"}]
