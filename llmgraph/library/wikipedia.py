import requests
from joblib import Memory
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

memory = Memory(".joblib_cache")


def _rest_v1_summary(url: str, redirect: bool = True):
    assert "wikipedia.org/wiki/" in url
    wiki_loc = url.rfind("/wiki/")
    page_title = url[wiki_loc:].replace(
        "/wiki/", ""
    )  # TODO: handle hashtag cases? e.g. Python_(programming_language)#Syntax_and_semantics

    redirect = "true" if redirect else "false"
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title}?redirect={redirect}"
    response = requests.get(url)
    status_code = response.status_code
    headers = response.headers
    if status_code == 200:
        try:
            response_json = response.json()
            canonical = response_json.get("titles", {}).get("canonical", None)
            normalized = response_json.get("titles", {}).get("normalized", None)
            summary = response_json.get("extract", None)
            # import json
            # logger.warning(f"{json.dumps(response_json, indent=4)=}")
            return status_code, response_json, canonical, normalized, summary, headers
        except Exception:
            # NOTE: Can occur with a page that redirects and has redirect=false
            return status_code, {}, None, None, None, headers
    else:
        logger.warning(f"Status code was: {status_code}")
        return status_code, {}, None, None, None, headers


@memory.cache()
@retry(wait=wait_exponential(multiplier=2, min=5, max=600), stop=stop_after_attempt(5))
def get_wikipedia_data(url):
    assert "wikipedia.org/wiki/" in url
    status_code, response_json, canonical, normalized, summary, headers = _rest_v1_summary(url, redirect=False)

    if status_code != 200:
        logger.exception(f"Error. Unexpected response code: {status_code} for url {url}")

    return summary, canonical, normalized, status_code
