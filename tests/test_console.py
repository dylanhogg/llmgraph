from llmgraph import console


def test_console_run1():
    console.run("software-engineering", "https://en.wikipedia.org/wiki/Unit_testing", levels=1)


def test_console_run2():
    console.run("food", "https://en.wikipedia.org/wiki/Bolognese_sauce", levels=3)
