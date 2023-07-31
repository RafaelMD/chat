import requests
import os
import json
from typing import Dict, List, Optional, Tuple, Union
from math import radians, sin, cos, sqrt, atan2
 
 
class CepLocator:
    def __init__(self):
        self.api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        self.url_base = "https://maps.googleapis.com/maps/api/geocode/json"

    def cep_to_lat_lng(self, cep: str) -> Tuple[float, float]:
        """
        Converts a Brazilian postal code (CEP) to latitude and longitude coordinates using the Google Maps Geocoding API.

        Args:
            cep (str): A Brazilian postal code (CEP) to be converted.

        Returns:
            JSON: containing the latitude and longitude coordinates of the given CEP.

        Raises:
            ValueError: If the CEP is not found or the API request fails.
        """
        parametros = {"address": cep, "key": self.api_key}
        resposta = requests.get(self.url_base, params=parametros)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            if dados['results']:
                localizacao = dados['results'][0]['geometry']['location']

                position = {
                    "lat": localizacao['lat'],
                    "lng": localizacao['lng']
                }
                return json.dumps(position)
            else:
                return json.dumps({"error": "CEP não encontrado"})
        else:
            return json.dumps({"error": "Tive uma falha na requisição ao buscar o CEP ({resposta.status_code})"})
 
    def export_function_cep(self):
        return {
            "name": "cep_to_lat_lng",
            "description": "Converts a Brazilian postal code (CEP) to latitude and longitude coordinates using the Google Maps Geocoding API",
            "parameters": {
                "type": "object",
                "properties": {
                    "cep": {
                        "type": "string",
                        "description": "cep (str): A Brazilian postal code (CEP) to be converted",
                    }
                },
                "required": ["cep"],
            },
        }
    
    def distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculates the distance between two points on the Earth's surface using the Haversine formula.

        Args:
            lat1 (float): The latitude of the first point in degrees.
            lon1 (float): The longitude of the first point in degrees.
            lat2 (float): The latitude of the second point in degrees.
            lon2 (float): The longitude of the second point in degrees.

        Returns:
            float: The distance between the two points in kilometers.

        Examples:
            >>> distance(52.2296756, 21.0122287, 52.406374, 16.9251681)
            278.54558935106695
        """
        R = 6373.0

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance_km = R * c

        return distance_km

    def search_places(self, lat: float, lng: float,  keyword: Optional[str] = None) -> List[Dict[str, Union[str, float]]]:
        """
        Searches for places near a given latitude and longitude using the Google Maps Places API.

        Args:
            lat (float): The latitude of the center point in degrees.
            lng (float): The longitude of the center point in degrees.
            keyword (str, optional): A term to be matched against all available fields, including but not limited to name, type, and address, of the places returned. Defaults to None.

        Returns:
            JSON: A list of dictionaries containing information about the places found, including name, latitude, longitude, and distance from the center point.

        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """
        radius = 5000
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

        params = {
            "key": self.api_key,
            "location": f"{lat},{lng}",
            "radius": radius
        }

        if keyword:
            params["keyword"] = keyword
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()["results"]
        places = []

        for result in results:
            place_lat = result["geometry"]["location"]["lat"]
            place_lng = result["geometry"]["location"]["lng"]
            place_distance = self.distance(lat, lng, place_lat, place_lng)
            place = {"name": result["name"], "lat": place_lat, "lng": place_lng, "distance": place_distance}
            places.append(place)

        # Sort places by distance from center point
        places.sort(key=lambda x: x["distance"])
        return json.dumps(places)

    def export_function_search_places(self):
        return {
            "name": "search_places",
            "description": "Searches for places near a given latitude and longitude using the Google Maps Places API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {
                        "type": "number",
                        "description": "The latitude of the center point in degrees.",
                    },
                    "lng": {
                        "type": "number",
                        "description": "The longitude of the center point in degrees.",
                    },
                    "keyword": {
                        "type": "string",
                        "description": "A term to be matched against all available fields, including but not limited to name, type, and address, of the places returned.",
                    },
                },
                "required": ["lat", "lng"],
            },
        }