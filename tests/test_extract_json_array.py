from llmgraph.library import utils


def test1() -> None:
    chat_response = '[\n  {\n    "name": "General Motors",\n    "wikipedia_link": "https://en.wikipedia.org/wiki/General_Motors",\n    "reason_for_similarity": "Both Ford and General Motors are major American automobile manufacturers with a long history and global presence.",\n    "similarity": 0.9\n  },\n  {\n    "name": "Toyota Motor Corporation",\n    "wikipedia_link": "https://en.wikipedia.org/wiki/Toyota",\n    "reason_for_similarity": "Toyota is one of the largest automobile manufacturers globally, similar to Ford\'s global presence.",\n    "similarity": 0.8\n  },\n  {\n    "name": "Volkswagen Group",\n    "wikipedia_link": "https://en.wikipedia.org/wiki/Volkswagen_Group",\n    "reason_for_similarity": "Volkswagen Group is a major automotive conglomerate with a diverse portfolio of brands, similar to Ford\'s portfolio.",\n    "similarity": 0.7\n  },\n  {\n    "name": "Honda Motor Company",\n    "wikipedia_link": "https://en.wikipedia.org/wiki/Honda",\n    "reason_for_similarity": "Honda is a renowned automobile manufacturer known for its innovation and global presence, similar to Ford.",\n    "similarity": 0.6\n  },\n  {\n    "name": "Hyundai Motor Company",\n    "wikipedia_link": "https://en.wikipedia.org/wiki/Hyundai_Motor_Company",\n    "reason_for_similarity": "Hyundai is a leading global automobile manufacturer with a wide range of vehicles, similar to Ford\'s product diversity.",\n    "similarity": 0.6\n  }\n]'
    json_array = utils.extract_json_array(chat_response)
    print(f"{json_array}")
    assert json_array


def test2() -> None:
    chat_response = 'test2 bla1 [\n  {\n    "name": "General Motors",\n    "wikipedia_link": "https://en.wikipedia.org/wiki/General_Motors",\n    "reason_for_similarity": "Both Ford and General Motors are major American automobile manufacturers with a long history and global presence.",\n    "similarity": 0.9\n  },\n  {\n    "name": "Toyota Motor Corporation",\n    "wikipedia_link": "https://en.wikipedia.org/wiki/Toyota",\n    "reason_for_similarity": "Toyota is one of the largest automobile manufacturers globally, similar to Ford\'s global presence.",\n    "similarity": 0.8\n  },\n  {\n    "name": "Volkswagen Group",\n    "wikipedia_link": "https://en.wikipedia.org/wiki/Volkswagen_Group",\n    "reason_for_similarity": "Volkswagen Group is a major automotive conglomerate with a diverse portfolio of brands, similar to Ford\'s portfolio.",\n    "similarity": 0.7\n  },\n  {\n    "name": "Honda Motor Company",\n    "wikipedia_link": "https://en.wikipedia.org/wiki/Honda",\n    "reason_for_similarity": "Honda is a renowned automobile manufacturer known for its innovation and global presence, similar to Ford.",\n    "similarity": 0.6\n  },\n  {\n    "name": "Hyundai Motor Company",\n    "wikipedia_link": "https://en.wikipedia.org/wiki/Hyundai_Motor_Company",\n    "reason_for_similarity": "Hyundai is a leading global automobile manufacturer with a wide range of vehicles, similar to Ford\'s product diversity.",\n    "similarity": 0.6\n  }\n] bla2'
    json_array = utils.extract_json_array(chat_response)
    print(f"{json_array}")
    assert json_array


def test3() -> None:
    chat_response = 'test3 bla3 [\n  {\n    "name": "General Motors"\n}]] bla4'
    json_array = utils.extract_json_array(chat_response)
    print(f"{json_array}")
    assert json_array


def test4() -> None:
    chat_response = (
        'test4 bla3 [\n  {\n    "name": "General Motors"\n}]] bla [\n  {\n    "name": "Missed json"\n}]] bla4'
    )
    json_array = utils.extract_json_array(chat_response)
    print(f"{json_array}")
    assert json_array
