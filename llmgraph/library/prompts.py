from omegaconf import OmegaConf


def _get_prompt_format(entity_type: str, yaml_file: str = "prompts.yaml"):
    conf_file = OmegaConf.load(yaml_file)
    # TODO: use dot acccessors...
    common_prompt_format = conf_file.common.prompt_format
    assert common_prompt_format
    entity_conf = conf_file[entity_type]
    prompt_format = common_prompt_format.format(
        knowledgeable_about=entity_conf.knowledgeable_about,
        top_n=entity_conf.top_n,
        entities=entity_conf.entities,
        entity=entity_conf.entity,
        entity_underscored=entity_conf.entity.replace(" ", "_"),
    )
    return prompt_format


def get(entity_root: str, entity_type: str, yaml_file: str = "prompts.yaml"):
    prompt_format = _get_prompt_format(entity_type, yaml_file)
    prompt = prompt_format.format(entity_root=entity_root)
    return prompt


def system(entity_type: str, yaml_file: str = "prompts.yaml"):
    conf_file = OmegaConf.load(yaml_file)
    entity_conf = conf_file[entity_type]
    return entity_conf.system
