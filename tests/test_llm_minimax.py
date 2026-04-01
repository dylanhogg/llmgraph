"""Tests for MiniMax provider support in llmgraph.library.llm."""
from unittest.mock import MagicMock, patch

import pytest
from omegaconf import OmegaConf

from llmgraph.library import consts
from llmgraph.library.llm import _is_minimax_model, _resolve_model_config, memory


# ---------------------------------------------------------------------------
# Unit tests: _is_minimax_model
# ---------------------------------------------------------------------------


class TestIsMiniMaxModel:
    def test_minimax_m27_detected(self):
        assert _is_minimax_model("minimax/MiniMax-M2.7") is True

    def test_minimax_m27_highspeed_detected(self):
        assert _is_minimax_model("minimax/MiniMax-M2.7-highspeed") is True

    def test_minimax_m25_detected(self):
        assert _is_minimax_model("minimax/MiniMax-M2.5") is True

    def test_minimax_m25_highspeed_detected(self):
        assert _is_minimax_model("minimax/MiniMax-M2.5-highspeed") is True

    def test_openai_model_not_minimax(self):
        assert _is_minimax_model("gpt-4o-mini") is False

    def test_openai_prefixed_minimax_model_not_minimax(self):
        assert _is_minimax_model("openai/MiniMax-M2.7") is False

    def test_ollama_model_not_minimax(self):
        assert _is_minimax_model("ollama/llama2") is False

    def test_empty_string_not_minimax(self):
        assert _is_minimax_model("") is False

    def test_claude_not_minimax(self):
        assert _is_minimax_model("anthropic/claude-3-opus") is False


# ---------------------------------------------------------------------------
# Unit tests: _resolve_model_config
# ---------------------------------------------------------------------------


class TestResolveModelConfig:
    def test_minimax_m27_routes_to_openai_compat(self):
        model, base_url, temp = _resolve_model_config("minimax/MiniMax-M2.7", None, 0.7)
        assert model == "openai/MiniMax-M2.7"

    def test_minimax_sets_default_base_url(self):
        _, base_url, _ = _resolve_model_config("minimax/MiniMax-M2.7", None, 0.7)
        assert base_url == consts.minimax_api_base

    def test_minimax_custom_base_url_preserved(self):
        _, base_url, _ = _resolve_model_config("minimax/MiniMax-M2.7", "https://custom.host/v1", 0.7)
        assert base_url == "https://custom.host/v1"

    def test_minimax_temp_zero_clamped_to_min(self):
        _, _, temp = _resolve_model_config("minimax/MiniMax-M2.7", None, 0.0)
        assert temp == 0.01

    def test_minimax_temp_one_preserved(self):
        _, _, temp = _resolve_model_config("minimax/MiniMax-M2.7", None, 1.0)
        assert temp == 1.0

    def test_minimax_temp_above_one_clamped_to_one(self):
        _, _, temp = _resolve_model_config("minimax/MiniMax-M2.7", None, 2.0)
        assert temp == 1.0

    def test_minimax_m25_highspeed_routes_correctly(self):
        model, _, _ = _resolve_model_config("minimax/MiniMax-M2.5-highspeed", None, 0.5)
        assert model == "openai/MiniMax-M2.5-highspeed"

    def test_non_minimax_model_unchanged(self):
        model, base_url, temp = _resolve_model_config("gpt-4o-mini", None, 1.0)
        assert model == "gpt-4o-mini"
        assert base_url is None
        assert temp == 1.0

    def test_ollama_model_unchanged(self):
        model, base_url, temp = _resolve_model_config("ollama/llama2", "http://localhost:11434", 0.8)
        assert model == "ollama/llama2"
        assert base_url == "http://localhost:11434"
        assert temp == 0.8

    def test_minimax_api_base_constant_format(self):
        assert consts.minimax_api_base.startswith("https://")
        assert "/v1" in consts.minimax_api_base


# ---------------------------------------------------------------------------
# Integration tests: make_call routes MiniMax correctly
# ---------------------------------------------------------------------------


def _make_mock_response(content="[]", total_tokens=10):
    mock = MagicMock()
    mock.choices = [MagicMock()]
    mock.choices[0].message.content = content
    mock.__getitem__ = MagicMock(side_effect=lambda key: {"total_tokens": total_tokens, "usage": {"total_tokens": total_tokens}}[key])
    mock.__class__.__getitem__ = mock.__getitem__
    return mock


class TestMakeCallMiniMaxIntegration:
    def setup_method(self):
        memory.clear(warn=False)

    def test_make_call_routes_minimax_model_to_openai_compat(self):
        """make_call should translate minimax/ prefix to openai/ for LiteLLM."""
        from llmgraph.library.llm import make_call

        llm_config = OmegaConf.create(
            {"model": "minimax/MiniMax-M2.7", "temperature": 0.7, "base_url": None, "delay": 0}
        )
        mock_response = _make_mock_response()
        mock_response["usage"] = {"total_tokens": 10}

        with patch("llmgraph.library.llm.completion", return_value=mock_response) as mock_comp:
            make_call("integration_test_entity_1", "sys", "prompt", llm_config)
            call_kwargs = mock_comp.call_args.kwargs
            assert call_kwargs["model"] == "openai/MiniMax-M2.7"
            assert call_kwargs["base_url"] == consts.minimax_api_base

    def test_make_call_clamps_zero_temperature_for_minimax(self):
        """make_call should clamp temperature=0 to 0.01 for MiniMax."""
        from llmgraph.library.llm import make_call

        llm_config = OmegaConf.create(
            {"model": "minimax/MiniMax-M2.7", "temperature": 0.0, "base_url": None, "delay": 0}
        )
        mock_response = _make_mock_response()
        mock_response["usage"] = {"total_tokens": 10}

        with patch("llmgraph.library.llm.completion", return_value=mock_response) as mock_comp:
            make_call("integration_test_entity_2", "sys", "prompt", llm_config)
            call_kwargs = mock_comp.call_args.kwargs
            assert call_kwargs["temperature"] == 0.01

    def test_make_call_non_minimax_model_passes_through(self):
        """Non-MiniMax models should pass model name and base_url unchanged."""
        from llmgraph.library.llm import make_call

        llm_config = OmegaConf.create(
            {"model": "gpt-4o-mini", "temperature": 1.0, "base_url": None, "delay": 0}
        )
        mock_response = _make_mock_response()
        mock_response["usage"] = {"total_tokens": 10}

        with patch("llmgraph.library.llm.completion", return_value=mock_response) as mock_comp:
            make_call("integration_test_entity_3", "sys", "prompt", llm_config)
            call_kwargs = mock_comp.call_args.kwargs
            assert call_kwargs["model"] == "gpt-4o-mini"
            assert call_kwargs["base_url"] is None
