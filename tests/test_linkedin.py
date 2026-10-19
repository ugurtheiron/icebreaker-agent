import pytest

from ice_breaker import SUMMARY_TEMPLATE
from third_parties import linkedin


def _no_network(*args, **kwargs):
    raise AssertionError("unexpected HTTP request")


def test_mock_profile_loads_offline_from_any_directory_and_fills_the_prompt(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)  # the sample path must not depend on the working directory
    monkeypatch.setattr(linkedin.requests, "get", _no_network)

    data = linkedin.scrape_linkedin_profile(mock=True)

    assert data["full_name"] == "Jane Doe"
    assert data["experiences"]
    assert "Jane Doe" in SUMMARY_TEMPLATE.format(information=data)


def test_live_mode_without_api_key_fails_before_any_request(monkeypatch):
    monkeypatch.delenv("PROXYCURL_API_KEY", raising=False)
    monkeypatch.setattr(linkedin.requests, "get", _no_network)

    with pytest.raises(RuntimeError, match="PROXYCURL_API_KEY"):
        linkedin.scrape_linkedin_profile("https://example.com/in/jane-doe-example/")


def test_live_mode_sends_key_from_environment_and_no_personal_contact_fields(monkeypatch):
    monkeypatch.setenv("PROXYCURL_API_KEY", "test-key")
    sent = {}

    class FakeResponse:
        def json(self):
            return {"full_name": "Jane Doe"}

    def fake_get(url, headers, params, timeout):
        sent.update(url=url, headers=headers, params=params)
        return FakeResponse()

    monkeypatch.setattr(linkedin.requests, "get", fake_get)

    data = linkedin.scrape_linkedin_profile("https://example.com/in/jane-doe-example/")

    assert data == {"full_name": "Jane Doe"}
    assert sent["url"] == linkedin.PROXYCURL_ENDPOINT
    assert sent["headers"]["Authorization"] == "Bearer test-key"
    assert sent["params"]["linkedin_profile_url"] == "https://example.com/in/jane-doe-example/"
    assert not {"personal_email", "personal_contact_number", "inferred_salary"} & set(sent["params"])
