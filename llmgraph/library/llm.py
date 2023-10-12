import time
from datetime import datetime

import openai
from joblib import Memory
from loguru import logger
from tenacity import retry, retry_if_not_exception_type, stop_after_attempt, wait_exponential

from . import env
from .classes import AppUsageException

memory = Memory(".joblib_cache")

# TODO: try/catch! E.g.
#       APIError: HTTP code 502 from API
#       Timeout: Request timed out: HTTPSConnectionPool(host='api.openai.com', port=443): Read timed out. (read timeout=600)


def log_retry(state):
    msg = (
        f"Tenacity retry {state.fn.__name__}: {state.attempt_number=}, {state.idle_for=}, {state.seconds_since_start=}"
    )
    if state.attempt_number < 1:
        logger.info(msg)
    else:
        logger.exception(msg)


@memory.cache()
@retry(
    wait=wait_exponential(multiplier=2, min=5, max=600),
    stop=stop_after_attempt(5),
    before_sleep=log_retry,
    retry=retry_if_not_exception_type(AppUsageException),
)
def make_call(entity: str, system: str, prompt: str, temperature: int, use_localhost: bool) -> (str, int):
    if use_localhost:
        openai.api_key = "localhost"
        openai.api_base = "http://localhost:8081"
        time.sleep(int(env.get("LLM_USE_LOCALHOST_SLEEP", 1)))
    else:
        try:
            key = env.get("OPENAI_API_KEY")
        except Exception as ex:
            raise AppUsageException("Expected environment variable OPENAI_API_KEY to be set to use OpenAI API.") from ex
        openai.api_key = key

    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]

    start = datetime.now()
    api_response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=temperature)
    took = datetime.now() - start

    chat_response = api_response.choices[0].message.content
    total_tokens = int(api_response["usage"]["total_tokens"])

    logger.trace(f"{use_localhost=}")
    logger.trace(f"{system=}")
    logger.trace(f"{prompt=}")
    logger.trace(f"{took=}")
    logger.trace("\n---- RESPONSE:")
    logger.trace(f"{chat_response=}")
    logger.trace(f"{total_tokens=}")

    return chat_response, total_tokens
