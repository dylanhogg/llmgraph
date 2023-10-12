import json
import urllib.parse
from typing import Optional

import networkx as nx
from loguru import logger
from tqdm import tqdm

from llmgraph.library.classes import AppUsageException

from . import consts, llm, prompts, utils, wikipedia

sum_total_tokens = 0


def _call_llm_on_entity(entity: str, entity_type: str, llm_temp: int, llm_use_localhost: int) -> Optional[list[dict]]:
    global sum_total_tokens
    prompt = prompts.get(entity, entity_type, consts.prompts_yaml_location)
    system = prompts.system(entity_type, consts.prompts_yaml_location)
    chat_response, total_tokens = llm.make_call(entity, system, prompt, llm_temp, llm_use_localhost)

    sum_total_tokens += total_tokens
    assert chat_response
    assert isinstance(chat_response, str)
    dict_list = utils.extract_json_array(chat_response)
    return dict_list


node_count = 0


def get_entity_name(wikipedia_link, name):
    entity_name = wikipedia_link if wikipedia_link else name
    wiki_loc = entity_name.rfind("/wiki/")
    if wiki_loc > -1:
        entity_name = entity_name[wiki_loc:].replace("/wiki/", "").replace("_", " ")
        entity_name = urllib.parse.unquote(entity_name)
    return entity_name


def _make_root_graph(source_entity: str, source_wikipedia: str) -> nx.DiGraph:
    G = nx.DiGraph()
    entity_name = get_entity_name(
        source_wikipedia, source_entity
    )  # TODO: refine and make like add_node in _add_to_graph

    summary, canonical, normalized, status_code = wikipedia.get_wikipedia_data(source_wikipedia)
    G.add_node(
        entity_name,  # TODO: or normalized?
        name=source_entity,
        level=0,
        wikipedia_link=source_wikipedia,
        wikipedia_canonical=canonical,
        wikipedia_normalized=normalized,
        wikipedia_resp_code=status_code,
        wikipedia_content=summary[0:500] if summary else "",  # TODO: review and sync with _add_to_graph(..)
        processed=utils.PROCESSED["UN"],
        node_count=0,
    )
    return G


def _add_to_graph(G: nx.DiGraph, level: int, source_entity: str, json_array: list[dict]):
    global node_count
    for entity in json_array:
        """
        Expected json template:
        {
            "name": "HarperCollins",
            "wikipedia_link": "https://en.wikipedia.org/wiki/HarperCollins",
            "reason_for_similarity": "Both are major book publishers with a long history and global reach.",
            "similarity": 0.8
        },
        """
        target_entity = get_entity_name(entity["wikipedia_link"], entity["name"])
        if target_entity not in list(G.nodes):
            # TODO: verify this approach, in particular, should we test for eq on wikipedia_link?

            summary, canonical, normalized, status_code = wikipedia.get_wikipedia_data(entity["wikipedia_link"])

            node_count += 1
            G.add_node(
                target_entity,  # TODO: or normalized?
                name=entity["name"],
                level=level + 1,
                wikipedia_link=entity["wikipedia_link"],
                wikipedia_canonical=canonical,
                wikipedia_normalized=normalized,
                wikipedia_resp_code=status_code,
                wikipedia_content=summary[0:500] if summary else "",  # TODO: review and sync with _make_root_graph(..)
                reason_for_similarity=entity["reason_for_similarity"],
                processed=utils.PROCESSED["UN"],
                node_count=node_count,
            )
        else:
            logger.debug(f"Node {target_entity} already exists")

        if source_entity != target_entity:
            # Ignore self loops
            G.add_edge(source_entity, target_entity, weight=entity["similarity"])

    return G


def _process_graph(
    entity_root: str,
    entity_type: str,
    level: int,
    G: nx.DiGraph,
    max_sum_total_tokens: int,
    output_folder: str,
    llm_temp: int,
    llm_use_localhost: int,
) -> nx.DiGraph:
    current_nodes = list(G.nodes.items()).copy()
    for node in current_nodes:
        # node=('Volkswagen Group', {'name': 'Volkswagen Group',
        # 'wikipedia_link': 'https://en.wikipedia.org/wiki/Volkswagen_Group',
        # 'processed': 0, 'group': 2, 'node_count': 13,
        # 'label': 'Volkswagen Group (#13, G2)', 'size': 10})
        # type(node)=<class 'tuple'>
        node_data = node[1]
        if not node_data["processed"]:
            logger.debug(
                f"Processing node: {node_data['name']}, {node_data['wikipedia_link']}, level {node_data['level']}"
            )
            source_entity = get_entity_name(node_data["wikipedia_link"], node_data["name"])
            llm_response_dict_list = _call_llm_on_entity(source_entity, entity_type, llm_temp, llm_use_localhost)
            approx_total_cost = (sum_total_tokens / 1000) * 0.002
            logger.info(
                f"Processed node '{source_entity}'. Sum total tokens for this run: {sum_total_tokens} (approx total cost ${approx_total_cost:,.4}, assuming gpt-3.5-turbo 4k model at Sep 2023 prices)"
            )
            if llm_response_dict_list:
                G = _add_to_graph(G, level, source_entity, llm_response_dict_list)
                G.nodes[source_entity]["processed"] = utils.PROCESSED["PR"]
                utils.write_html(
                    output_folder, entity_type, entity_root, level, G, llm_temp, llm_use_localhost, processed_only=True
                )
                utils.write_html(
                    output_folder, entity_type, entity_root, level, G, llm_temp, llm_use_localhost, processed_only=False
                )
                try:
                    utils.write_graphml(output_folder, entity_type, entity_root, level, G, llm_temp, llm_use_localhost)
                except Exception as ex:
                    logger.error(
                        f"write_graphml error processing {source_entity=} with {json.dumps(llm_response_dict_list, indent=2)=}"
                    )
                    raise ex
            else:
                # TODO: Retry, with increased temperature?
                G.nodes[source_entity]["processed"] = utils.PROCESSED["ER"]
                return G

    if sum_total_tokens > max_sum_total_tokens:
        raise AppUsageException(f"Token limit hit: {sum_total_tokens=}, {max_sum_total_tokens=}")

    return G


def create_company_graph(
    entity_type: str,
    entity: str,
    entity_wikipedia: str,
    levels: int,
    max_sum_total_tokens: int,
    output_folder: str,
    llm_temp: int,
    llm_use_localhost: int,
) -> nx.DiGraph:
    G = _make_root_graph(entity, entity_wikipedia)

    pbar = tqdm(range(1, levels + 1))
    for level in pbar:
        pbar.set_description(f"Processing level {level}")
        logger.debug(f"Processing {level=}")
        G = _process_graph(
            entity, entity_type, level, G, max_sum_total_tokens, output_folder, llm_temp, llm_use_localhost
        )

    return G
