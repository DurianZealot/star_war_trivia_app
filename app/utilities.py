import requests


def search_characters_from_swapi(api, name):
    """Search characters by name from given api 

    Args:
        api (str): API endpoint
        name (str): name to search

    Returns:
        Dict: {character_name : {"name": "xx", "films": ["f1"], "vehicles": ["v1"]}}
    """
    swapi = f"{api}{name}"
    character_film_vehicles = {}
    try:
        response = requests.get(swapi, timeout=1)  # timeout 1s
        response.raise_for_status()
        data = response.json()
        result_count = data["count"]
        while data["results"] != []:
            for res in data["results"]:
                character_name = res["name"]
                character_movies = res["films"]
                character_vehicles = res["vehicles"]
                character_film_vehicles[character_name] = {
                    "name": character_name, "films": character_movies, "vehicles": character_vehicles}
            if data["next"] is not None:
                try:
                    response = requests.get(data["next"], timeout=1)
                    response.raise_for_status()
                    data = response.json()
                except requests.exceptions.Timeout:
                    print("Request Timeout")
                    return character_film_vehicles
                except requests.exceptions.RequestException as e:
                    print(f"Request Failure:{e}")
                    return character_film_vehicles
            else:
                break
        print(f"{result_count}:{len(character_film_vehicles)}")
        return character_film_vehicles
    except requests.exceptions.Timeout:
        print("Request Timeout")
    except requests.exceptions.RequestException as e:
        print(f"Request Failure:{e}")
    return character_film_vehicles


def search_vehicles_in_film(film_link, vehicles):
    """Match all vehicles that one character drives shows in a given film 

    Args:
        film_link (str): an endpoint to give all details of a given film
        vehicles (List[str]): a list of vehicle links

    Returns:
        List[str]: A list of all vehicles driven by one character shows in a given film 
    """
    try:
        response = requests.get(film_link, timeout=1)  # timeout 1s
        response.raise_for_status()
        data = response.json()
        vehicles_in_film = data["vehicles"]
        vehicles_in_film_character = list(
            set(vehicles_in_film).intersection(vehicles))
        return vehicles_in_film_character
    except requests.exceptions.Timeout:
        print("Request Timeout")
    except requests.exceptions.RequestException as e:
        print(f"Request Failure:{e}")
    return []


def get_film_title(film):
    """
    Retrieve the title of a film from the given API link.

    Parameters:
    film (str): The API link for the film.

    Returns:
    str: The title of the film, or film API link if the request fails.

    Exceptions:
    If an HTTP error, timeout, or other request exception occurs, an error message will be printed.
    """
    try:
        response = requests.get(film, timeout=1)  # timeout 1 seconds
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        return data["title"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    return film  # Return film API link if an error occurs

def get_vehicle_model(vehicle):
    """
    Retrieve the model of a vehicle from the given API link.

    Parameters:
    vehicle (str): The API link for the vehicle.

    Returns:
    str: The model of the vehicle, or vehicle link if the request fails.

    Exceptions:
    If an HTTP error, timeout, or other request exception occurs, an error message will be printed.
    """
    try:
        response = requests.get(vehicle, timeout=1)  # timeout 1 seconds
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        return data["model"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
    return vehicle  # Return vehicle link if an error occurs

def match_vehicles_w_film(character_film_vehicles):
    """ Match films with vehicles

    Args:
        character_film_vehicles (Dict): 
            {character_name : {"name": "xx", "films": ["f1"], "vehicles": ["v1"]}}

    Returns:
        Dict: {character_name : {"name": "xx", "films": ["f1"], "vehicles": ["v1"], "film_vehicle_match":{"f1": ["v1"]}}}
    """
    for character, vehicles_films_dict in character_film_vehicles.items():
        film_vehicles_matching = {}

        films = vehicles_films_dict["films"]
        vehicles = vehicles_films_dict["vehicles"]

        for film in films:
            film_title = get_film_title(film)
            matched_vehicles = search_vehicles_in_film(film, vehicles)
            vehicle_models_lst = []
            for vehicle in matched_vehicles:
                vehicle_models_lst.append(get_vehicle_model(vehicle))
            film_vehicles_matching[film_title] = vehicle_models_lst
        vehicles_films_dict["film_vehicle_match"] = film_vehicles_matching
    return character_film_vehicles
