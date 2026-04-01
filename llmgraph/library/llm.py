from datetime import datetime
from time import sleep

from joblib import Memory
from litellm import completion
from loguru import logger
from omegaconf import DictConfig
from tenacity import retry, retry_if_not_exception_type, stop_after_attempt, wait_exponential

from . import consts
from .classes import AppUsageException

memory = Memory(".joblib_cache", verbose=0)

# TODO: try/catch! E.g.
#       APIError: HTTP code 502 from API
#       Timeout: Request timed out: HTTPSConnectionPool(host='api.openai.com', port=443): Read timed out. (read timeout=600)


def _is_minimax_model(model: str) -> bool:
    """Return True if the model name uses the 'minimax/' provider prefix."""
    return model.startswith(consts.minimax_model_prefix)


def _resolve_model_config(model: str, base_url, temperature: float):
    """Resolve provider-specific model name, base URL, and temperature.

    For MiniMax models (``minimax/<name>``):
    - Routes via LiteLLM's OpenAI-compatible path (``openai/<name>``).
    - Sets the MiniMax base URL when none is provided.
    - Clamps temperature to (0.0, 1.0] as required by the MiniMax API.
    """
    if _is_minimax_model(model):
        model_name = model[len(consts.minimax_model_prefix):]
        resolved_base_url = base_url if base_url else consts.minimax_api_base
        clamped_temp = max(0.01, min(1.0, temperature))
        return f"openai/{model_name}", resolved_base_url, clamped_temp
    return model, base_url, temperature


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
def make_call(entity: str, system: str, prompt: str, llm_config: DictConfig) -> (str, int):
    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    start = datetime.now()

    model, base_url, temperature = _resolve_model_config(
        llm_config.model, llm_config.base_url, llm_config.temperature
    )

    try:
        api_response = completion(
            model=model,
            messages=messages,
            temperature=temperature,
            base_url=base_url,
        )
    except Exception as ex:
        logger.exception(f"Exception from LLM call: {ex}")
        raise AppUsageException(str(ex)) from ex

    took = datetime.now() - start
    sleep(llm_config.delay)

    chat_response = api_response.choices[0].message.content
    total_tokens = int(api_response["usage"]["total_tokens"])

    logger.trace(f"{llm_config.base_url=}")
    logger.trace(f"{system=}")
    logger.trace(f"{prompt=}")
    logger.trace(f"{took=}")
    logger.trace("\n---- RESPONSE:")
    logger.trace(f"{chat_response=}")
    logger.trace(f"{total_tokens=}")

    return chat_response, total_tokens
