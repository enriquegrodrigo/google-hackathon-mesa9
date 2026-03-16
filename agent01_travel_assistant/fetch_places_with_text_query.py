#
# Copyright (c) 2025 Google Cloud.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
import os

import requests
from dotenv import load_dotenv
from utils import format_opening_hours

PLACES_API_TEXT_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"


def fetch_places_with_text_query(
    text_query: str,
) -> str:
    """
    Internal function to fetch places and return a formatted string for the LLM.
    Includes Place ID if available.
    """
    max_results = 7
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    print(f"--- Tool: Fetching places for query: '{text_query}' ---")
    if not api_key:
        return "Error: Google Maps API key is not configured."
    if not text_query:
        return "Error: text_query cannot be empty."

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "*",  # "places.id,places.displayName,places.formattedAddress,places.types,places.rating,places.userRatingCount,places.priceLevel",
    }
    request_body = {
        "textQuery": text_query,
        "maxResultCount": min(max_results, 20),
        "languageCode": "en",
    }

    try:
        response = requests.post(
            PLACES_API_TEXT_SEARCH_URL,
            headers=headers,
            data=json.dumps(request_body),
            timeout=15,
        )
        response.raise_for_status()
        results = response.json()
        places = results.get("places", [])
        if not places:
            return "No places found matching the query."

        formatted_places = []
        for i, place in enumerate(places):
            place_id = place.get("id", "N/A")
            name = place.get("displayName", {}).get("text", "N/A")
            address = place.get("formattedAddress", "N/A")
            types = ", ".join(place.get("types", ["N/A"]))
            rating = place.get("rating", "N/A")
            geometry = place.get("geometry", {})
            count = place.get("userRatingCount", "N/A")
            price = place.get("priceLevel", "N/A")
            opening_hours = place.get("currentOpeningHours", {})
            formatted_places.append(
                f"{i+1}. Name: {name}\n  Place ID: {place_id}\n  Address: {address}\n   Latitude: {geometry.get('location', {}).get('latitude', 'N/A')}, Longitude: {geometry.get('location', {}).get('longitude', 'N/A')}\n   Type(s): {types}\n   Rating: {rating} ({count} reviews)\n   Price Level: {price}\n Opening Hours: {format_opening_hours(opening_hours)}"
            )
        return "Found the following potential places:\n\n" + "\n\n".join(
            formatted_places
        )

    except requests.exceptions.RequestException as e:
        error_msg = f"Error fetching places from Google Maps API: {e}"
        try:
            error_details = response.json()
            error_msg += f"\nAPI Error Details: {error_details}"
        except:
            pass
        print(error_msg)
        return f"Error: Could not fetch places. {e}"
    except Exception as e:
        print(f"An unexpected error occurred fetching places: {e}")
        return f"Error: An unexpected error occurred while fetching places. {e}"


if __name__ == "__main__":
    load_dotenv()

    SEARCH_QUERY = "good places for French cuisine in Paris close to the Google office, 25 Rue de Clichy"

    resp = fetch_places_with_text_query(text_query=SEARCH_QUERY)

    print(resp)
