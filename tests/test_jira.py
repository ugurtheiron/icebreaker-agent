from third_parties import jira


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self):
        return self._payload


def test_issue_fields_are_extracted_including_unassigned_issues(monkeypatch):
    payload = {
        "key": "PROJ-1",
        "fields": {
            "summary": "Fix the login page",
            "created": "2025-01-10T09:00:00.000+0000",
            "assignee": None,  # Jira sends null for an unassigned issue
            "priority": {"name": "High"},
            "status": {"name": "In Progress"},
            "issuelinks": [
                {"outwardIssue": {"key": "PROJ-2"}},
                {"inwardIssue": {"key": "PROJ-3"}},
            ],
        },
    }
    seen = {}

    def fake_get(url, headers):
        seen.update(url=url, headers=headers)
        return FakeResponse(payload=payload)

    monkeypatch.setattr(jira.requests, "get", fake_get)

    details = jira.get_jira_issue_details("https://jira.example.com", "PROJ-1", "token")

    assert seen["url"] == "https://jira.example.com/rest/api/2/issue/PROJ-1"
    assert seen["headers"]["Authorization"] == "Bearer token"
    assert details == {
        "key": "PROJ-1",
        "summary": "Fix the login page",
        "created": "2025-01-10T09:00:00.000+0000",
        "assignee": "Unassigned",
        "priority": "High",
        "status": "In Progress",
        "related_issues": ["PROJ-2"],
    }


def test_http_error_is_returned_as_error_dict(monkeypatch):
    monkeypatch.setattr(
        jira.requests, "get", lambda url, headers: FakeResponse(status_code=404, text="Not Found")
    )

    details = jira.get_jira_issue_details("https://jira.example.com", "PROJ-404", "token")

    assert "Status Code: 404" in details["error"]
