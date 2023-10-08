import json
import re
from pathlib import Path
from typing import Optional
from urllib.parse import unquote

import matplotlib.pyplot as plt
import networkx as nx
import requests
from bs4 import BeautifulSoup
from joblib import Memory
from loguru import logger
from pyvis.network import Network

from . import consts, env

memory = Memory(".joblib_cache")

PROCESSED = {
    "UN": 0,  # Unproocessed
    "PR": 2,  # Processed
    "ER": 3,  # Error in processing, skipped
}


def _clean_entity_name(name: str):
    return name.lower().replace(" ", "-").replace("/", "-")


def _get_wiki_name(wikipedia_link: str):
    loc = wikipedia_link.rfind("/wiki/")
    return wikipedia_link if loc == -1 else wikipedia_link[loc:].replace("/wiki/", "")


def _get_ui_wiki_name(wikipedia_link: str):
    loc = wikipedia_link.rfind("/wiki/")
    assert loc > 0
    wiki_name = wikipedia_link[loc:].replace("/wiki/", "").replace("_", " ")
    return unquote(wiki_name)


def _add_visual_attributes(G):
    current_nodes = list(G.nodes.items()).copy()
    for node in current_nodes:
        entity = node[0]
        # name = G.nodes[entity]["name"]  # TODO: maybe reuse again? Esp case if there is no wikipedia link available(?)
        level = G.nodes[entity]["level"]  # TODO
        processed = G.nodes[entity]["processed"]
        node_count = G.nodes[entity]["node_count"]
        wikipedia_link = G.nodes[entity]["wikipedia_link"]
        wikipedia_resp_code = G.nodes[entity]["wikipedia_resp_code"]
        wikipedia_content = G.nodes[entity]["wikipedia_content"]

        group = 0  # Root
        if node_count > 0 and processed == PROCESSED["PR"]:
            group = 1  # Processed
        elif node_count > 0 and processed == PROCESSED["UN"]:
            group = 2  # Not processed yet
        elif node_count > 0 and processed == PROCESSED["ER"]:
            group = 3  # Error

        # TODO: handle case if there is no wikipedia link available(?)
        wikipedia_name = _get_ui_wiki_name(wikipedia_link)

        G.nodes[entity]["label"] = f"{wikipedia_name}"  # Label is displayed on node in UI
        # G.nodes[entity]["level"] = level  # NOTE: used in some hierarchical physics layouts
        G.nodes[entity]["group"] = level  # TODO: Or use group?
        G.nodes[entity][
            "title"
        ] = f"#{node_count}. <a href='{wikipedia_link}' target='_blank'>{_get_wiki_name(wikipedia_link)}</a> (G{group}, L{level})<br />{wikipedia_content} [{wikipedia_resp_code}]"

    # TODO: edge labels...
    # current_edges = list(G.edges.items()).copy()
    # for edge in current_edges:
    #     entity = edge[0]
    #     name = G.edges[entity]
    #     G.edges[entity]["label"] = name

    return G


def _get_output_path(output_folder: str, entity_type: str, entity_root: str):
    output_path = Path(output_folder) / entity_type / _clean_entity_name(entity_root)
    Path(output_path).mkdir(parents=True, exist_ok=True)
    return output_path


def write_html(
    output_folder: str, entity_type: str, entity_root: str, level: int, G, processed_only: bool, min_level: int = 1
):
    if level < min_level:
        return

    temperature = float(env.get("LLM_TEMPERATURE"))
    use_localhost = int(env.get("LLM_USE_LOCALHOST"))
    output_path = _get_output_path(output_folder, entity_type, entity_root)
    file_name = f"{entity_type}_{_clean_entity_name(entity_root)}_v{consts.version}_LH{use_localhost}_L{level}_T{temperature}.html"

    G = _add_visual_attributes(G)

    if processed_only:
        nodes = [node for node, data in G.nodes(data=True) if data.get("processed") == PROCESSED["PR"]]
        G = G.subgraph(nodes)
        file_name = file_name.replace(".html", "_PROCESSED_ONLY.html")

    nt = Network(height="1000px", width="100%", directed=True, cdn_resources="remote")
    nt.from_nx(G)
    # nt.barnes_hut(gravity=-80000, central_gravity=0.3, spring_length=250, spring_strength=0.001, damping=0.09, overlap=0)  # https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.barnes_hut
    nt.force_atlas_2based(
        spring_strength=0.03
    )  # default spring_strength=0.08; https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.force_atlas_2based
    nt.show_buttons(filter_=["physics"])
    nt.write_html(str(output_path / file_name), open_browser=False, notebook=False)


def write_graphml(output_folder: str, entity_type: str, entity_root: str, level: int, G, min_level: int = 1):
    if level < min_level:
        return

    temperature = float(env.get("LLM_TEMPERATURE"))
    use_localhost = int(env.get("LLM_USE_LOCALHOST"))
    output_path = _get_output_path(output_folder, entity_type, entity_root)
    nx.write_graphml(
        G,
        f"{output_path}/{entity_type}_{_clean_entity_name(entity_root)}_v{consts.version}_LH{use_localhost}_L{level}_T{temperature}.graphml",
    )
    nx.write_gexf(
        G,
        f"{output_path}/{entity_type}_{_clean_entity_name(entity_root)}_v{consts.version}_LH{use_localhost}_L{level}_T{temperature}.gephi.gexf",
    )


def extract_json_array(text) -> Optional[list[dict]]:
    text = text.replace("\n", "").replace("\r", "")
    pattern = r"\[.*?\]"
    match = re.search(pattern, text)
    if match:
        json_array = match.group()
        try:
            parsed_array = json.loads(json_array)
            logger.trace(f"extract_json_array success:\n" + json.dumps(parsed_array, indent=4))
            return parsed_array
        except json.JSONDecodeError as ex:
            logger.warning(f"extract_json_array: {ex} {text=}")
            return None
    else:
        logger.warning(f"extract_json_array: no matches for {pattern=}. {text=}")
        return None
