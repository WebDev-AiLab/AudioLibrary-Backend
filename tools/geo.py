import requests

GEOCODING_URL = 'https://nominatim.openstreetmap.org/search'


def GEO_search_coordinates_by_location(location: str):
    params = {
        'q': location,
        'format': 'json'
    }
    try:
        response = requests.get(GEOCODING_URL, params)
        response = response.json()
        if response and response[0]:
            return response[0]
    except:
        return None
