from utilities import search_characters_from_api, search_characters
import pytest
import json
from mocket.mockhttp import Entry
from mocket import Mocketizer
from mocket.exceptions import StrictMocketException

import sys
import os
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')))


@pytest.fixture
def mock_response_palpatine():
    return {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "name": "Palpatine",
                "height": "170",
                "mass": "75",
                "hair_color": "grey",
                "skin_color": "pale",
                "eye_color": "yellow",
                "birth_year": "82BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/8/",
                "films": [
                        "https://swapi.dev/api/films/2/",
                        "https://swapi.dev/api/films/3/",
                        "https://swapi.dev/api/films/4/",
                        "https://swapi.dev/api/films/5/",
                        "https://swapi.dev/api/films/6/"
                ],
                "species": [],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-15T12:48:05.971000Z",
                "edited": "2014-12-20T21:17:50.347000Z",
                "url": "https://swapi.dev/api/people/21/"
            }
        ]
    }


def test_success(mock_response_palpatine):
    api = "https://swapi.dev/api/people?search="
    name = "Palpatine"

    Entry.single_register(
        Entry.GET,
        f"{api}{name}",
        body=json.dumps(mock_response_palpatine),
        headers={'content-type': 'application/json'}
    )

    with Mocketizer():
        mocked_response = search_characters_from_api(api, name)
        mocked_final_result = search_characters(api, name)

    assert mocked_response == {name: {"name": name, "films": [
        "https://swapi.dev/api/films/2/",
        "https://swapi.dev/api/films/3/",
        "https://swapi.dev/api/films/4/",
        "https://swapi.dev/api/films/5/",
        "https://swapi.dev/api/films/6/"
    ],
        "vehicles": []}}
    assert mocked_final_result == {name: {"name": name, "films": [
        "https://swapi.dev/api/films/2/",
        "https://swapi.dev/api/films/3/",
        "https://swapi.dev/api/films/4/",
        "https://swapi.dev/api/films/5/",
        "https://swapi.dev/api/films/6/"
    ],
        "vehicles": [], "film_vehicle_match": {"The Empire Strikes Back": [], "Return of the Jedi": [], "The Phantom Menace": [], "Attack of the Clones": [], "Revenge of the Sith": []}}}


@pytest.fixture
def mock_response_skywalker():
    return {
        "count": 3,
        "next": None,
        "previous": None,
        "results": [
            {
                "name": "Luke Skywalker",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/2/",
                    "https://swapi.dev/api/films/3/",
                    "https://swapi.dev/api/films/6/"
                ],
                "species": [],
                "vehicles": [
                    "https://swapi.dev/api/vehicles/14/",
                    "https://swapi.dev/api/vehicles/30/"
                ],
                "starships": [
                    "https://swapi.dev/api/starships/12/",
                    "https://swapi.dev/api/starships/22/"
                ],
                "created": "2014-12-09T13:50:51.644000Z",
                "edited": "2014-12-20T21:17:56.891000Z",
                "url": "https://swapi.dev/api/people/1/"
            },
            {
                "name": "Anakin Skywalker",
                "height": "188",
                "mass": "84",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "41.9BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": [
                    "https://swapi.dev/api/films/4/",
                    "https://swapi.dev/api/films/5/",
                    "https://swapi.dev/api/films/6/"
                ],
                "species": [],
                "vehicles": [
                    "https://swapi.dev/api/vehicles/44/",
                    "https://swapi.dev/api/vehicles/46/"
                ],
                "starships": [
                    "https://swapi.dev/api/starships/39/",
                    "https://swapi.dev/api/starships/59/",
                    "https://swapi.dev/api/starships/65/"
                ],
                "created": "2014-12-10T16:20:44.310000Z",
                "edited": "2014-12-20T21:17:50.327000Z",
                "url": "https://swapi.dev/api/people/11/"
            },
            {
                "name": "Shmi Skywalker",
                "height": "163",
                "mass": "unknown",
                "hair_color": "black",
                "skin_color": "fair",
                "eye_color": "brown",
                "birth_year": "72BBY",
                "gender": "female",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": [
                    "https://swapi.dev/api/films/4/",
                    "https://swapi.dev/api/films/5/"
                ],
                "species": [],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-19T17:57:41.191000Z",
                "edited": "2014-12-20T21:17:50.401000Z",
                "url": "https://swapi.dev/api/people/43/"
            }
        ]
    }


def test_success_3matches(mock_response_skywalker):
    api = "https://swapi.dev/api/people?search="
    name = "Skywalker"

    Entry.single_register(
        Entry.GET,
        f"{api}{name}",
        body=json.dumps(mock_response_skywalker),
        headers={'content-type': 'application/json'}
    )

    with Mocketizer():
        mocked_response = search_characters_from_api(api, name)
        mocked_final_response = search_characters(api, name)

        expect_resp = {
            "Luke Skywalker": {
                "name": "Luke Skywalker",
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/2/",
                    "https://swapi.dev/api/films/3/",
                    "https://swapi.dev/api/films/6/"
                ],
                "vehicles": [
                    "https://swapi.dev/api/vehicles/14/",
                    "https://swapi.dev/api/vehicles/30/"
                ]
            },
            "Anakin Skywalker": {
                "name": "Anakin Skywalker",
                "films": [
                    "https://swapi.dev/api/films/4/",
                    "https://swapi.dev/api/films/5/",
                    "https://swapi.dev/api/films/6/"
                ],
                "vehicles": [
                    "https://swapi.dev/api/vehicles/44/",
                    "https://swapi.dev/api/vehicles/46/"
                ]
            },
            "Shmi Skywalker": {
                "name": "Shmi Skywalker",
                "films": [
                    "https://swapi.dev/api/films/4/",
                    "https://swapi.dev/api/films/5/"
                ],
                "vehicles": []
            }
        }
        expect_final_resp = {
            "Luke Skywalker": {
                "name": "Luke Skywalker",
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/2/",
                    "https://swapi.dev/api/films/3/",
                    "https://swapi.dev/api/films/6/"
                ],
                "vehicles": [
                    "https://swapi.dev/api/vehicles/14/",
                    "https://swapi.dev/api/vehicles/30/"
                ],
                "film_vehicle_match": {
                    "A New Hope": [],
                    "The Empire Strikes Back": ["t-47 airspeeder"],
                    "Return of the Jedi": ["74-Z speeder bike"],
                    "Revenge of the Sith": []
                }
            },
            "Anakin Skywalker": {
                "name": "Anakin Skywalker",
                "films": [
                    "https://swapi.dev/api/films/4/",
                    "https://swapi.dev/api/films/5/",
                    "https://swapi.dev/api/films/6/"
                ],
                "vehicles": [
                    "https://swapi.dev/api/vehicles/44/",
                    "https://swapi.dev/api/vehicles/46/"
                ],
                "film_vehicle_match": {
                    "The Phantom Menace": [],
                    "Attack of the Clones": ['Zephyr-G swoop bike', 'XJ-6 airspeeder'],
                    "Revenge of the Sith": []
                }
            },
            "Shmi Skywalker": {
                "name": "Shmi Skywalker",
                "films": [
                    "https://swapi.dev/api/films/4/",
                    "https://swapi.dev/api/films/5/"
                ],
                "vehicles": [],
                "film_vehicle_match": {
                    "The Phantom Menace": [],
                    "Attack of the Clones": []
                }
            }
        }
    assert mocked_response == expect_resp
    assert mocked_final_response == expect_final_resp


@pytest.fixture
def mock_response_null():
    return {
        "count": 0,
        "next": None,
        "previous": None,
        "results": []
    }


def test_null(mock_response_null):
    api = "https://swapi.dev/api/people?search="
    name = "NULL"
    Entry.single_register(
        Entry.GET,
        f"{api}{name}",
        body=json.dumps(mock_response_null),
        headers={'content-type': 'application/json'}
    )

    with Mocketizer():
        mocked_response = search_characters_from_api(api, name)
        mocked_final_response = search_characters(api, name)

    assert mocked_response == {}
    assert mocked_final_response == {}


@pytest.fixture
def mock_response_matches_page1():
    return {
        "count": 15,
        "next": "https://swapi.dev/api/people/?search=H&page=2",
        "previous": None,
        "results": [
            {
                "name": "Darth Vader",
                "height": "202",
                "mass": "136",
                "hair_color": "none",
                "skin_color": "white",
                "eye_color": "yellow",
                "birth_year": "41.9BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/2/",
                    "https://swapi.dev/api/films/3/",
                    "https://swapi.dev/api/films/6/"
                ],
                "species": [],
                "vehicles": [],
                "starships": [
                    "https://swapi.dev/api/starships/13/"
                ],
                "created": "2014-12-10T15:18:20.704000Z",
                "edited": "2014-12-20T21:17:50.313000Z",
                "url": "https://swapi.dev/api/people/4/"
            },
            {
                "name": "Beru Whitesun lars",
                "height": "165",
                "mass": "75",
                "hair_color": "brown",
                "skin_color": "light",
                "eye_color": "blue",
                "birth_year": "47BBY",
                "gender": "female",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/5/",
                    "https://swapi.dev/api/films/6/"
                ],
                "species": [],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-10T15:53:41.121000Z",
                "edited": "2014-12-20T21:17:50.319000Z",
                "url": "https://swapi.dev/api/people/7/"
            },
            {
                "name": "Biggs Darklighter",
                "height": "183",
                "mass": "84",
                "hair_color": "black",
                "skin_color": "light",
                "eye_color": "brown",
                "birth_year": "24BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": [
                    "https://swapi.dev/api/films/1/"
                ],
                "species": [],
                "vehicles": [],
                "starships": [
                    "https://swapi.dev/api/starships/12/"
                ],
                "created": "2014-12-10T15:59:50.509000Z",
                "edited": "2014-12-20T21:17:50.323000Z",
                "url": "https://swapi.dev/api/people/9/"
            },
            {
                "name": "Wilhuff Tarkin",
                "height": "180",
                "mass": "unknown",
                "hair_color": "auburn, grey",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "64BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/21/",
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/6/"
                ],
                "species": [],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-10T16:26:56.138000Z",
                "edited": "2014-12-20T21:17:50.330000Z",
                "url": "https://swapi.dev/api/people/12/"
            },
            {
                "name": "Chewbacca",
                "height": "228",
                "mass": "112",
                "hair_color": "brown",
                "skin_color": "unknown",
                "eye_color": "blue",
                "birth_year": "200BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/14/",
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/2/",
                    "https://swapi.dev/api/films/3/",
                    "https://swapi.dev/api/films/6/"
                ],
                "species": [
                    "https://swapi.dev/api/species/3/"
                ],
                "vehicles": [
                    "https://swapi.dev/api/vehicles/19/"
                ],
                "starships": [
                    "https://swapi.dev/api/starships/10/",
                    "https://swapi.dev/api/starships/22/"
                ],
                "created": "2014-12-10T16:42:45.066000Z",
                "edited": "2014-12-20T21:17:50.332000Z",
                "url": "https://swapi.dev/api/people/13/"
            },
            {
                "name": "Han Solo",
                "height": "180",
                "mass": "80",
                "hair_color": "brown",
                "skin_color": "fair",
                "eye_color": "brown",
                "birth_year": "29BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/22/",
                "films": [
                    "https://swapi.dev/api/films/1/",
                    "https://swapi.dev/api/films/2/",
                    "https://swapi.dev/api/films/3/"
                ],
                "species": [],
                "vehicles": [],
                "starships": [
                    "https://swapi.dev/api/starships/10/",
                    "https://swapi.dev/api/starships/22/"
                ],
                "created": "2014-12-10T16:49:14.582000Z",
                "edited": "2014-12-20T21:17:50.334000Z",
                "url": "https://swapi.dev/api/people/14/"
            },
            {
                "name": "Mon Mothma",
                "height": "150",
                "mass": "unknown",
                "hair_color": "auburn",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "48BBY",
                "gender": "female",
                "homeworld": "https://swapi.dev/api/planets/32/",
                "films": [
                    "https://swapi.dev/api/films/3/"
                ],
                "species": [],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-18T11:12:38.895000Z",
                "edited": "2014-12-20T21:17:50.364000Z",
                "url": "https://swapi.dev/api/people/28/"
            },
            {
                "name": "Quarsh Panaka",
                "height": "183",
                "mass": "unknown",
                "hair_color": "black",
                "skin_color": "dark",
                "eye_color": "brown",
                "birth_year": "62BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/8/",
                "films": [
                    "https://swapi.dev/api/films/4/"
                ],
                "species": [],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-19T17:55:43.348000Z",
                "edited": "2014-12-20T21:17:50.399000Z",
                "url": "https://swapi.dev/api/people/42/"
            },
            {
                "name": "Shmi Skywalker",
                "height": "163",
                "mass": "unknown",
                "hair_color": "black",
                "skin_color": "fair",
                "eye_color": "brown",
                "birth_year": "72BBY",
                "gender": "female",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": [
                    "https://swapi.dev/api/films/4/",
                    "https://swapi.dev/api/films/5/"
                ],
                "species": [],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-19T17:57:41.191000Z",
                "edited": "2014-12-20T21:17:50.401000Z",
                "url": "https://swapi.dev/api/people/43/"
            },
            {
                "name": "Darth Maul",
                "height": "175",
                "mass": "80",
                "hair_color": "none",
                "skin_color": "red",
                "eye_color": "yellow",
                "birth_year": "54BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/36/",
                "films": [
                    "https://swapi.dev/api/films/4/"
                ],
                "species": [
                    "https://swapi.dev/api/species/22/"
                ],
                "vehicles": [
                    "https://swapi.dev/api/vehicles/42/"
                ],
                "starships": [
                    "https://swapi.dev/api/starships/41/"
                ],
                "created": "2014-12-19T18:00:41.929000Z",
                "edited": "2014-12-20T21:17:50.403000Z",
                "url": "https://swapi.dev/api/people/44/"
            }
        ]
    }


@pytest.fixture
def mock_response_matches_page2():
    return {
        "count": 15,
        "next": None,
        "previous": "https://swapi.dev/api/people/?search=H&page=1",
        "results": [
            {
                "name": "Eeth Koth",
                "height": "171",
                "mass": "unknown",
                "hair_color": "black",
                "skin_color": "brown",
                "eye_color": "brown",
                "birth_year": "unknown",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/45/",
                "films": [
                    "https://swapi.dev/api/films/4/",
                    "https://swapi.dev/api/films/6/"
                ],
                "species": [
                    "https://swapi.dev/api/species/22/"
                ],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-20T10:26:47.902000Z",
                "edited": "2014-12-20T21:17:50.427000Z",
                "url": "https://swapi.dev/api/people/54/"
            },
            {
                "name": "Gregar Typho",
                "height": "185",
                "mass": "85",
                "hair_color": "black",
                "skin_color": "dark",
                "eye_color": "brown",
                "birth_year": "unknown",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/8/",
                "films": [
                    "https://swapi.dev/api/films/5/"
                ],
                "species": [],
                "vehicles": [],
                "starships": [
                    "https://swapi.dev/api/starships/39/"
                ],
                "created": "2014-12-20T11:10:10.381000Z",
                "edited": "2014-12-20T21:17:50.445000Z",
                "url": "https://swapi.dev/api/people/60/"
            },
            {
                "name": "Poggle the Lesser",
                "height": "183",
                "mass": "80",
                "hair_color": "none",
                "skin_color": "green",
                "eye_color": "yellow",
                "birth_year": "unknown",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/11/",
                "films": [
                    "https://swapi.dev/api/films/5/",
                    "https://swapi.dev/api/films/6/"
                ],
                "species": [
                    "https://swapi.dev/api/species/28/"
                ],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-20T16:40:43.977000Z",
                "edited": "2014-12-20T21:17:50.453000Z",
                "url": "https://swapi.dev/api/people/63/"
            },
            {
                "name": "San Hill",
                "height": "191",
                "mass": "unknown",
                "hair_color": "none",
                "skin_color": "grey",
                "eye_color": "gold",
                "birth_year": "unknown",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/57/",
                "films": [
                    "https://swapi.dev/api/films/5/"
                ],
                "species": [
                    "https://swapi.dev/api/species/34/"
                ],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-20T17:58:17.049000Z",
                "edited": "2014-12-20T21:17:50.484000Z",
                "url": "https://swapi.dev/api/people/77/"
            },
            {
                "name": "Shaak Ti",
                "height": "178",
                "mass": "57",
                "hair_color": "none",
                "skin_color": "red, blue, white",
                "eye_color": "black",
                "birth_year": "unknown",
                "gender": "female",
                "homeworld": "https://swapi.dev/api/planets/58/",
                "films": [
                    "https://swapi.dev/api/films/5/",
                    "https://swapi.dev/api/films/6/"
                ],
                "species": [
                    "https://swapi.dev/api/species/35/"
                ],
                "vehicles": [],
                "starships": [],
                "created": "2014-12-20T18:44:01.103000Z",
                "edited": "2014-12-20T21:17:50.486000Z",
                "url": "https://swapi.dev/api/people/78/"
            }
        ]
    }


def test_multipages(mock_response_matches_page1, mock_response_matches_page2):
    api = "https://swapi.dev/api/people?search="
    name = "H"

    Entry.single_register(
        Entry.GET,
        f"{api}{name}",
        body=json.dumps(mock_response_matches_page1),
        headers={'content-type': 'application/json'}
    )

    Entry.single_register(
        Entry.GET,
        "https://swapi.dev/api/people/?search=H&page=2",
        body=json.dumps(mock_response_matches_page2),
        headers={'content-type': 'application/json'}
    )

    with Mocketizer():
        mocked_response = search_characters_from_api(api, name)

    assert mocked_response == {
        "Eeth Koth": {
            "name": "Eeth Koth",
            "films": [
                "https://swapi.dev/api/films/4/",
                "https://swapi.dev/api/films/6/"
            ],
            "vehicles": []
        },
        "Gregar Typho": {
            "name": "Gregar Typho",
            "films": [
                "https://swapi.dev/api/films/5/"
            ],
            "vehicles": []
        },
        "Poggle the Lesser": {
            "name": "Poggle the Lesser",
            "films": [
                "https://swapi.dev/api/films/5/",
                "https://swapi.dev/api/films/6/"
            ],
            "vehicles": []
        },
        "San Hill": {
            "name": "San Hill",
            "films": [
                "https://swapi.dev/api/films/5/"
            ],
            "vehicles": []
        },
        "Shaak Ti": {
            "name": "Shaak Ti",
            "films": [
                "https://swapi.dev/api/films/5/",
                "https://swapi.dev/api/films/6/"
            ],
            "vehicles": []
        },
        "Darth Vader": {
            "name": "Darth Vader",
            "films": [
                "https://swapi.dev/api/films/1/",
                "https://swapi.dev/api/films/2/",
                "https://swapi.dev/api/films/3/",
                "https://swapi.dev/api/films/6/"
            ],
            "vehicles": []
        },
        "Beru Whitesun lars": {
            "name": "Beru Whitesun lars",
            "films": [
                "https://swapi.dev/api/films/1/",
                "https://swapi.dev/api/films/5/",
                "https://swapi.dev/api/films/6/"
            ],
            "vehicles": []
        },
        "Biggs Darklighter": {
            "name": "Biggs Darklighter",
            "films": [
                "https://swapi.dev/api/films/1/"
            ],
            "vehicles": []
        },
        "Wilhuff Tarkin": {
            "name": "Wilhuff Tarkin",
            "films": [
                "https://swapi.dev/api/films/1/",
                "https://swapi.dev/api/films/6/"
            ],
            "vehicles": []
        },
        "Chewbacca": {
            "name": "Chewbacca",
            "films": [
                "https://swapi.dev/api/films/1/",
                "https://swapi.dev/api/films/2/",
                "https://swapi.dev/api/films/3/",
                "https://swapi.dev/api/films/6/"
            ],
            "vehicles": [
                "https://swapi.dev/api/vehicles/19/"
            ]
        },
        "Han Solo": {
            "name": "Han Solo",
            "films": [
                "https://swapi.dev/api/films/1/",
                "https://swapi.dev/api/films/2/",
                "https://swapi.dev/api/films/3/"
            ],
            "vehicles": []
        },
        "Mon Mothma": {
            "name": "Mon Mothma",
            "films": [
                "https://swapi.dev/api/films/3/"
            ],
            "vehicles": []
        },
        "Quarsh Panaka": {
            "name": "Quarsh Panaka",
            "films": [
                "https://swapi.dev/api/films/4/"
            ],
            "vehicles": [],
        },
        "Shmi Skywalker": {
            "name": "Shmi Skywalker",
            "films": [
                "https://swapi.dev/api/films/4/",
                "https://swapi.dev/api/films/5/"
            ],
            "vehicles": []
        },
        "Darth Maul": {
            "name": "Darth Maul",
            "films": [
                "https://swapi.dev/api/films/4/"
            ],
            "vehicles": [
                "https://swapi.dev/api/vehicles/42/"
            ]
        }
    }


def test_timeout():
    with Mocketizer(strict_mode=True):
        with pytest.raises(StrictMocketException):
            response = search_characters_from_api(
                "https://swapi.dev/api/people/?search=", "ANY")
            final_response = search_characters(
                "https://swapi.dev/api/people/?search=", "ANY")
            assert response == {}
            assert final_response == {}
