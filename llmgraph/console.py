import os
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from omegaconf import OmegaConf
from rich import print
from typing_extensions import Annotated

from .library import consts, engine, env, log, utils
from .library.classes import AppUsageException

typer_app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(f"llmgraph version: {consts.version}")
        raise typer.Exit()


def open_in_browser(concept_output_folder: Path):
    while True:
        files = [f for f in os.listdir(concept_output_folder) if "fully_connected" in f]
        if len(files) == 0:
            break
        filename = concept_output_folder / sorted(files)[-1]
        print(f"Fully connected html file: '{filename}'")
        user_input = input("Press 'Y' to open the fully connected html file in a browser, or Enter/Return to finish: ")
        if user_input.lower() == "y":
            abs_file = filename.resolve()
            webbrowser.open(f"file://{abs_file}")
            break
        elif user_input.lower() == "":
            break


@typer_app.command()
def run(
    entity_type: Annotated[str, typer.Argument(help="Entity type (e.g. movie)")],
    entity_wikipedia: Annotated[str, typer.Argument(help="Full wikipedia link to root entity")],
    entity_root: Annotated[
        str, typer.Option(help="Optional root entity name override if different from wikipedia page title")
    ] = None,
    levels: Annotated[int, typer.Option(help="Number of levels deep to construct from the central root entity")] = 2,
    max_sum_total_tokens: Annotated[int, typer.Option(help="Maximum sum of tokens for graph generation")] = 200000,
    output_folder: Annotated[str, typer.Option(help="Folder location to write outputs")] = consts.default_output_folder,
    llm_model: Annotated[str, typer.Option(help="The model name")] = consts.default_llm_model,
    llm_temp: Annotated[float, typer.Option(help="LLM temperature value")] = consts.default_llm_temp,
    llm_base_url: Annotated[str, typer.Option(help="LLM will use custom base URL instead of the automatic one")] = None,
    allow_user_input: Annotated[bool, typer.Option(help="Allow command line user input")] = True,
    version: Annotated[
        Optional[bool], typer.Option("--version", help="Display llmgraph version", callback=version_callback)
    ] = None,
) -> None:
    """
    Create knowledge graphs with LLMs
    """
    log.configure()

    example_usage = 'Example usage: [bold green]llmgraph movie "https://en.wikipedia.org/wiki/The_Matrix"[/bold green]'

    try:
        if "/wiki/" in entity_type:
            print(example_usage)
            raise AppUsageException("You appear to have the 'entity_type' and 'entity_wikipedia' arguments mixed up.")

        custom_entity_root = True
        if "/wiki/" not in entity_wikipedia:
            print(example_usage)
            raise AppUsageException(f"'{entity_wikipedia}' doesn't look like a valid wikipedia url.")
        if not entity_root:
            wiki_loc = entity_wikipedia.rfind("/wiki/")
            entity_root = entity_wikipedia[wiki_loc:].replace("/wiki/", "").replace("_", " ")  # TODO: review
            custom_entity_root = False

        print(
            f"Running with {entity_type=}, {entity_wikipedia=}, {entity_root=}, {custom_entity_root=}, {levels=}, {llm_model=}, {llm_temp=}, {output_folder=}"
        )

        if levels > 4:
            print(
                f"[bold orange3]Running with {levels=} - this will take many LLM calls, watch your costs if using a paid API![/bold orange3]"
            )
            print(
                "[bold orange3]It is recommended to start with levels=3 and build up since calls are cached with the same input parameter values.[/bold orange3]"
            )

            if allow_user_input:
                print(f"[bold orange3]Press Y to continue with {levels=}...[/bold orange3]")
                if input().lower() != "y":
                    raise AppUsageException(f"User did not press Y to continue running with {levels=}.")

        start = datetime.now()

        llm_config = OmegaConf.create(
            {
                "version": consts.version,
                "model": llm_model,
                "temperature": llm_temp,
                "base_url": llm_base_url,
                "delay": int(env.get("LLM_DELAY", 0)),
            }
        )

        engine.create_company_graph(
            entity_type,
            entity_root,
            entity_wikipedia,
            levels,
            max_sum_total_tokens,
            output_folder,
            llm_config,
        )

        took = datetime.now() - start
        concept_output_folder = utils.get_output_path(output_folder, entity_type, entity_root)
        print("")
        print(f"[bold green]llmgraph finished, took {took.total_seconds()}s.[/bold green]")
        print(f"Output written to folder '{concept_output_folder}' which includes, for each level:")
        print(" - An html file with only processed nodes as a fully connected graph")
        print(" - An html file with both processed and extra unprocessed edge nodes")
        print(" - A .graphml file (see http://graphml.graphdrawing.org/)")
        print(" - A .gefx file, good for viewing in gephi (see https://gexf.net/ and https://gephi.org/)")
        print("")
        if allow_user_input:
            open_in_browser(concept_output_folder)
            print("")
        print(
            "Thank you for using llmgraph! Please consider starring the project on github: https://github.com/dylanhogg/llmgraph"
        )

    except AppUsageException as ex:
        print(f"[bold red]{str(ex)}[/bold red]")
        print("")
        print("For more information, try 'llmgraph --help'.")

    except Exception as ex:
        print(f"[bold red]Unexpected exception: {str(ex)}[/bold red]")
        print("")
        print("For more information, try 'llmgraph --help'.")
