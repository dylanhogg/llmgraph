import importlib.resources

from omegaconf import OmegaConf

from llmgraph.library import consts
from llmgraph.library.classes import AppUsageException


def _get_conf(entity_type: str, yaml_file: str) -> (str, dict):
    yaml_file = importlib.resources.files(consts.package_name).joinpath(yaml_file)
    conf_file = OmegaConf.load(yaml_file)
    common_prompt_format = conf_file._common.prompt_format
    if not common_prompt_format:
        raise Exception(f"configfile {yaml_file} expected to have a common.prompt_format string")
    assert common_prompt_format
    if entity_type not in conf_file:
        valid_entity_types = sorted(
            [k for k in conf_file.keys() if not k.startswith("_") and not k.startswith("unit_test")]
        )
        raise AppUsageException(f"Entity type '{entity_type}' not supported. Try one of these: {valid_entity_types}")
    entity_conf = conf_file[entity_type]
    return common_prompt_format, entity_conf


def _get_prompt_format(entity_type: str, yaml_file: str):
    common_prompt_format, entity_conf = _get_conf(entity_type, yaml_file)
    prompt_format = common_prompt_format.format(
        knowledgeable_about=entity_conf.knowledgeable_about,
        top_n=entity_conf.top_n,
        entities=entity_conf.entities,
        entity=entity_conf.entity,
        entity_underscored=entity_conf.entity.replace(" ", "_"),
    )
    return prompt_format


def get(entity_root: str, entity_type: str, yaml_file: str):
    prompt_format = _get_prompt_format(entity_type, yaml_file)
    prompt = prompt_format.format(entity_root=entity_root)
    return prompt


def system(entity_type: str, yaml_file: str):
    yaml_file = importlib.resources.files(consts.package_name).joinpath(yaml_file)
    conf_file = OmegaConf.load(yaml_file)
    entity_conf = conf_file[entity_type]
    return entity_conf.system
