import requests


def get_location(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "version": response.get("version"),
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "timezone": response.get("timezone"),
        "latitude": response.get("latitude"),
        "longitude": response.get("longitude"),
        "utc_offset": response.get("utc_offset"),
    }
    return location_data
