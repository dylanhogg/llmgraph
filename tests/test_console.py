from llmgraph import console


def test_console_run():
    console.run("creative-general", "https://en.wikipedia.org/wiki/Diversity_and_inclusion", levels=1)
