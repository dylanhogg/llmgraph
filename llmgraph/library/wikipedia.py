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
    rest_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title}?redirect={redirect}"
    response = requests.get(rest_url)
    status_code = response.status_code
    headers = response.headers
    if status_code == 200:
        try:
            response_json = response.json()
            canonical = response_json.get("titles", {}).get("canonical", "")
            normalized = response_json.get("titles", {}).get("normalized", "")
            summary = response_json.get("extract", "")
            # import json
            # logger.warning(f"{json.dumps(response_json, indent=4)=}")
            return status_code, response_json, canonical, normalized, summary, headers
        except Exception:
            # NOTE: Can occur with a page that redirects and has redirect=false
            return status_code, {}, "", "", "", headers
    else:
        return status_code, {}, "", "", "", headers


@memory.cache()
@retry(wait=wait_exponential(multiplier=2, min=5, max=600), stop=stop_after_attempt(5))
def get_wikipedia_data(url) -> (str, str, str, int):
    if "wikipedia.org/wiki/" not in url:
        logger.info(f"Cannot get wikipedia data for {url=}")
        return "", "", "", -1

    redirect = True  # Ensure we resolve any wikipedia page redirects
    status_code, response_json, canonical, normalized, summary, headers = _rest_v1_summary(url, redirect=redirect)

    canonical = canonical if canonical else ""
    normalized = normalized if normalized else ""
    summary = summary if summary else ""

    assert canonical is not None, "canonical was None"
    assert normalized is not None, "normalized was None"
    assert status_code is not None, "status_code was None"
    assert response_json is not None, "response_json was None"
    assert summary is not None, "summary was None"
    assert headers is not None, "headers was None"

    if status_code != 200:
        logger.debug(f"Unsuccessful request: {status_code=} for {url=}")

    return summary, canonical, normalized, status_code
