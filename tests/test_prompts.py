from omegaconf import OmegaConf
from omegaconf.dictconfig import DictConfig
from loguru import logger
from llmgraph.library import prompts


def test_prompts_0():
    conf = OmegaConf.load("prompts.yaml")
    assert conf
    assert type(conf) == DictConfig


def test_prompts_1():
    conf = OmegaConf.load("prompts.yaml")
    assert conf["unit_test1"]["system"] == "You are an expert test driven developer."
    assert conf.unit_test1.system == conf["unit_test1"]["system"]
    assert conf.unit_test1.knowledgeable_about == "unit tests and testing frameworks"

    common_prompt_format = conf.common.prompt_format
    assert common_prompt_format

    # You are knowledgeable about {{knowledgeable_about}}.
    # List, in json array format, the top {top_n} {entities} most like '{entity}'
    # with Wikipedia link, reasons for similarity, similarity on scale of 0 to 1.
    # Format your response in json array format as an array with column names: 'name', 'wikipedia_link', 'reason_for_similarity', and 'similarity'.
    # Example response: {{"name": "Example {entity}","wikipedia_link": "https://en.wikipedia.org/wiki/Example_{entity_underscored}","reason_for_similarity": "Reason for similarity","similarity": 0.5}}
    prompt_format = common_prompt_format.format(
        knowledgeable_about=conf.unit_test1.knowledgeable_about,
        top_n=conf.unit_test1.top_n,
        entities=conf.unit_test1.entities,
        entity=conf.unit_test1.entity,
        entity_underscored=conf.unit_test1.entity.replace(" ", "_"),
    )
    assert prompt_format
    print(prompt_format)
    assert (
        prompt_format
        == """You are knowledgeable about unit tests and testing frameworks. List, in json array format, the top 5 unit test frameworks most like '{entity_root}' with Wikipedia link, reasons for similarity, similarity on scale of 0 to 1. Format your response in json array format as an array with column names: 'name', 'wikipedia_link', 'reason_for_similarity', and 'similarity'. Example response: {{"name": "Example unit test framework","wikipedia_link": "https://en.wikipedia.org/wiki/Example_unit_test_framework","reason_for_similarity": "Reason for similarity","similarity": 0.5}}"""
    )


def test_prompts_2():
    prompt_format = prompts._get_prompt_format("unit_test1")
    assert prompt_format
    assert (
        prompt_format
        == """You are knowledgeable about unit tests and testing frameworks. List, in json array format, the top 5 unit test frameworks most like '{entity_root}' with Wikipedia link, reasons for similarity, similarity on scale of 0 to 1. Format your response in json array format as an array with column names: 'name', 'wikipedia_link', 'reason_for_similarity', and 'similarity'. Example response: {{"name": "Example unit test framework","wikipedia_link": "https://en.wikipedia.org/wiki/Example_unit_test_framework","reason_for_similarity": "Reason for similarity","similarity": 0.5}}"""
    )


def test_prompts_3():
    prompt = prompts.get("pytest", "unit_test1")
    assert prompt
    assert (
        prompt
        == """You are knowledgeable about unit tests and testing frameworks. List, in json array format, the top 5 unit test frameworks most like 'pytest' with Wikipedia link, reasons for similarity, similarity on scale of 0 to 1. Format your response in json array format as an array with column names: 'name', 'wikipedia_link', 'reason_for_similarity', and 'similarity'. Example response: {"name": "Example unit test framework","wikipedia_link": "https://en.wikipedia.org/wiki/Example_unit_test_framework","reason_for_similarity": "Reason for similarity","similarity": 0.5}"""
    )
