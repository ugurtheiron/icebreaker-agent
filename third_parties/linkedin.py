"""Fetch LinkedIn profile data (Proxycurl API) or load a bundled sample.

Derived from third_parties/linkedin.py of Eden Marco's LangChain course
(https://github.com/emarco177/langchain-course, Apache-2.0, see NOTICE).
Changed by Uğur Özdemir: mock mode reads a local synthetic JSON file, the
Proxycurl request parameters, and the API key is validated before the call.
"""

import json
from pathlib import Path

import requests
from dotenv import load_dotenv

from env_utils import require_env

load_dotenv()

PROXYCURL_ENDPOINT = "https://nubela.co/proxycurl/api/v2/linkedin"
SAMPLE_PROFILE_PATH = Path(__file__).parent / "linkedin_profiles" / "sample_profile.json"


def scrape_linkedin_profile(linkedin_profile_url: str | None = None, mock: bool = False):
    """
    scrape information from LinkedIn profiles,
    Manually scrape the information from LinkedIn profiles.

    With ``mock=True`` the bundled synthetic profile is returned and no request is made.
    """

    if mock:
        with open(SAMPLE_PROFILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

    else:
        header_dic = {"Authorization": f"Bearer {require_env('PROXYCURL_API_KEY')}"}
        params = {
            "linkedin_profile_url": linkedin_profile_url,
            "extra": "include",
            "skills": "include",
            "use_cache": "if-present",
            "fallback_to_cache": "on-error",
        }
        response = requests.get(
            PROXYCURL_ENDPOINT,
            headers=header_dic,
            params=params,
            timeout=10,
        )
        data = response.json()

    return data


if __name__ == "__main__":
    print(scrape_linkedin_profile(mock=True))
