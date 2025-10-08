from llmgraph.library import wikipedia


def test_restapi_no_redirect_page():
    def do_asserts(status_code, response_json, canonical, normalized, summary, headers):
        assert status_code == 200
        assert response_json != {}
        assert canonical == page
        assert (
            "A neural network is a group of interconnected units called neurons that send signals to one another."
            in summary
        )
        assert response_json["titles"]["canonical"] == page
        assert canonical == page
        assert response_json["titles"]["normalized"] == page.replace("_", " ")
        assert normalized == page.replace("_", " ")
        assert page == response_json["titles"]["canonical"]

    page = "Neural_network"  # Page is direct, no redirect required

    status_code, response_json, canonical, normalized, summary, headers = wikipedia._rest_v1_summary(
        "https://en.wikipedia.org/wiki/" + page, redirect=False
    )
    do_asserts(status_code, response_json, canonical, normalized, summary, headers)

    status_code, response_json, canonical, normalized, summary, headers = wikipedia._rest_v1_summary(
        "https://en.wikipedia.org/wiki/" + page, redirect=True
    )
    do_asserts(status_code, response_json, canonical, normalized, summary, headers)


def test_restapi_redirect_page():
    page = "Neural_networks"  # Page redirects to:
    redirect_to_page = "Neural_network"
    expected_text = (
        "A neural network is a group of interconnected units called neurons that send signals to one another."
    )

    status_code, response_json, canonical, normalized, summary, headers = wikipedia._rest_v1_summary(
        "https://en.wikipedia.org/wiki/" + page, redirect=True
    )  # This is the one to use, check j["titles"]["canonical"] for rediect cases
    assert status_code == 200
    assert response_json != {}
    assert canonical != page
    assert canonical == redirect_to_page
    assert response_json["titles"]["normalized"] == redirect_to_page.replace("_", " ")
    assert normalized == redirect_to_page.replace("_", " ")
    assert "content-location" not in headers
    assert page != response_json["titles"]["canonical"]
    assert redirect_to_page == response_json["titles"]["canonical"]
    assert expected_text in summary
    assert response_json["titles"]["canonical"] != page
    assert response_json["titles"]["canonical"] == redirect_to_page
    assert canonical == redirect_to_page

    status_code, response_json, canonical, normalized, summary, headers = wikipedia._rest_v1_summary(
        "https://en.wikipedia.org/wiki/" + page, redirect=False
    )
    assert status_code == 200
    assert response_json != {}
    # NOTE: Oct 2025: Now redirect=False calls return the resolved page in json payload, as per above
    assert canonical != page
    assert canonical == redirect_to_page
    assert response_json["titles"]["normalized"] == redirect_to_page.replace("_", " ")
    assert normalized == redirect_to_page.replace("_", " ")
    assert expected_text in summary
    assert response_json["titles"]["canonical"] != page
    assert response_json["titles"]["canonical"] == redirect_to_page
    assert canonical == redirect_to_page


def test_get_resolved_wiki_page():
    # Tuples of [(requested page, resolved page), ...]
    page_resolved = [
        ("Neural_networks", "Neural_network"),
        ("Neural_network", "Neural_network"),
        ("Hydraulic", "Hydraulics"),
        ("Information_entropy", "Entropy_(information_theory)"),
        ("Python_(programming_language)", "Python_(programming_language)"),
    ]

    def _resolve(page):
        status_code, response_json, canonical, normalized, summary, headers = wikipedia._rest_v1_summary(
            "https://en.wikipedia.org/wiki/" + page, redirect=True
        )
        # NOTE: Oct 2025. Key "content-location" is now missing. We can now get resolved title from json after auto redirect
        # resolved = headers["content-location"].replace("https://en.wikipedia.org/api/rest_v1/page/summary/", "")  # Oct 2025: Key now missing
        assert "content-location" not in headers
        resolved = response_json["titles"]["canonical"]  # Oct 2025: Get resolved title from json

        return status_code, resolved

    for page, expected_resolved in page_resolved:
        status_code, actual_resolved = _resolve(page)
        assert status_code == 200
        assert expected_resolved == actual_resolved


# NOTES: (Old pre-Oct 2025 changes for auto redirect that has new page in json payload)
# https://en.wikipedia.org/api/rest_v1/#/Page%20content/get_page_title__title_

# https://en.wikipedia.org/api/rest_v1/page/title/Neural_network
# {
#   "items": [
#     {
#       "title": "Neural_network",
#       "page_id": 1729542,
#       "rev": 1176652345,
#       "tid": "80fa7660-5df6-11ee-93b9-093f0f607b7a",
#       "namespace": 0,
#       "user_id": 2615838,
#       "user_text": "Mikael Häggström",
#       "timestamp": "2023-09-23T03:29:15Z",
#       "comment": "+Purpose",
#       "tags": [
#         "wikieditor"
#       ],
#       "restrictions": [],
#       "page_language": "en",
#       "redirect": false
#     }
#   ]
# }

# https://en.wikipedia.org/api/rest_v1/page/title/Neural_networks
# {
#   "items": [
#     {
#       "title": "Neural_networks",
#       "page_id": 21524,
#       "rev": 843469194,
#       "tid": "a88a06a0-5df6-11ee-a969-5fd4b06acee6",
#       "namespace": 0,
#       "user_id": 14383484,
#       "user_text": "Wbm1058",
#       "timestamp": "2018-05-29T10:24:29Z",
#       "comment": "{{R from plural}}",
#       "tags": [],
#       "restrictions": [],
#       "page_language": "en",
#       "redirect": true
#     }
#   ]
# }

# https://en.wikipedia.org/w/api.php?action=parse&page=Neural_network&format=json
