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
import re
from datetime import datetime

import googlemaps
from dotenv import load_dotenv
from utils import format_directions_to_markdown


def _get_directions_logic(
    origin: str,
    destination: str,
    mode: str = "driving",
    departure_time: datetime | None = None,
) -> str:
    print(
        f"--- Tool Logic: Requesting directions - Origin: '{origin}', Destination: '{destination}', "
        f"Mode: '{mode}', Departure Time: {departure_time or 'default (now)'} ---"
    )

    if not origin or not destination:
        return "Error: Origin and Destination parameters cannot be empty."

    if not mode:
        print("Warning: Mode parameter was empty, defaulting to 'driving'.")
        mode = "driving"
    else:
        mode = mode.lower()
        valid_modes = ["driving", "walking", "bicycling", "transit"]
        if mode not in valid_modes:
            print(
                f"Warning: Invalid mode '{mode}' specified. API might reject or default. Valid modes: {valid_modes}"
            )

    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        print("Error: GOOGLE_MAPS_API_KEY environment variable not set.")
        return "Error: Google Maps API key is not configured."

    try:
        gmaps = googlemaps.Client(key=api_key)
    except Exception as e:
        print(f"Error initializing Google Maps client: {e}")
        return f"Error: Failed to initialize Google Maps client: {e}"

    api_params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "departure_time": departure_time,
    }

    try:
        print(
            f"--- Tool Logic: Calling Google Maps Directions API with params: {api_params} ---"
        )

        if mode == "driving" or mode == "transit":
            directions_result = gmaps.directions(
                origin=origin,
                destination=destination,
                mode=mode,
                departure_time=departure_time,
            )
        else:
            directions_result = gmaps.directions(
                origin=origin,
                destination=destination,
                mode=mode,
            )

        if not directions_result:
            print(
                f"Warning: No route found between '{origin}' and '{destination}' using mode '{mode}'. API returned empty result."
            )
            return f"No {mode} route found between '{origin}' and '{destination}'."

        if not directions_result[0].get("legs"):
            print(
                f"Warning: Directions result for '{origin}' to '{destination}' lacks 'legs'. Result: {directions_result}"
            )
            return f"Could not extract route details (legs) from the directions result between '{origin}' and '{destination}' for mode '{mode}'."

        leg = directions_result[0]["legs"][0]

        duration = leg.get("duration", {}).get("text", "N/A")
        distance = leg.get("distance", {}).get("text", "N/A")
        summary = directions_result[0].get("summary", "")
        start_address = leg.get("start_address", origin)
        end_address = leg.get("end_address", destination)

        directions_markdown = format_directions_to_markdown(directions_result)

        print(
            f"--- Tool Logic: Directions successfully retrieved: Duration={duration}, Distance={distance} ---"
        )

        return (
            f"Directions Result: Mode={mode}, "
            f"Origin='{start_address}' (Input: '{origin}'), "
            f"Destination='{end_address}' (Input: '{destination}'), "
            f"Duration={duration}, Distance={distance}, Summary='{summary}'",
            f"Directions='{directions_markdown}'",
        )

    except googlemaps.exceptions.ApiError as e:
        print(f"Error: Google Maps Directions API error: {e.status} - {e.message}")
        if e.status == "ZERO_RESULTS":
            return f"No {mode} route could be found between '{origin}' and '{destination}' (API status: ZERO_RESULTS)."
        elif e.status == "NOT_FOUND":
            return f"Could not geocode origin or destination: '{origin}' or '{destination}' (API status: NOT_FOUND)."
        return f"Error: API error occurred while getting directions: {e.status} - {e.message}"
    except googlemaps.exceptions.Timeout as e:
        print(f"Error: Google Maps Directions API request timed out: {e}")
        return "Error: The request to Google Maps timed out."
    except googlemaps.exceptions.TransportError as e:
        print(
            f"Error: Google Maps Directions transport error (e.g., network issue): {e}"
        )
        return f"Error: Network or transport issue communicating with Google Maps: {e}"
    except ValueError as e:
        print(f"Error processing location input: {e}")
        return f"Error: Could not process origin/destination input: {e}"
    except Exception as e:
        print(
            f"Error: An unexpected error occurred getting directions between '{origin}' and '{destination}': {e}"
        )
        return f"Error: An unexpected error occurred while getting directions: {e}"


def get_directions_tool_wrapper(json_input_string: str) -> str:
    """Wrapper function to parse JSON input for the directions tool."""
    try:
        cleaned_json_string = json_input_string.strip()  # Basic whitespace strip
        match = re.search(r"(\{.*\})|(\[.*\])", cleaned_json_string, re.DOTALL)
        if match:
            extracted_json = match.group(1) if match.group(1) else match.group(2)
        else:
            extracted_json = cleaned_json_string

        params = json.loads(extracted_json)

        origin = params.get("origin")
        destination = params.get("destination")
        mode = params.get("mode", "driving")
        departure_time_str = params.get("departure_time")

        departure_time = None

        if departure_time_str:
            try:
                departure_time = datetime.fromisoformat(departure_time_str)
            except ValueError:
                return (
                    f"Error: Invalid format for 'departure_time' key in JSON input: '{departure_time_str}'. "
                    f"Please use ISO 8601 format (e.g., 'YYYY-MM-DDTHH:MM:SS')."
                )
            except Exception as e:
                return f"Error parsing 'departure_time': {e}"

        if not origin or not destination:
            return "Error: JSON input must contain 'origin' and 'destination' keys."

        return _get_directions_logic(
            origin=origin,
            destination=destination,
            mode=mode,
            departure_time=departure_time,
        )

    except json.JSONDecodeError:
        return f"Error: Invalid JSON input string received: '{json_input_string}'. Please provide a valid JSON object."
    except KeyError as e:
        return f"Error: Missing required key in JSON input: {e}. Required keys: 'origin', 'destination'."
    except Exception as e:
        print(f"Error in tool wrapper: {e}")
        return f"Error processing directions request: {e}"


if __name__ == "__main__":
    load_dotenv()

    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S")

    query = f'{{"origin": "Schiphol Airport", "destination": "NH Hotel, the Hague", \
           "mode": "transit", "departure_time": "{formatted_date}", "transit_mode": "train"}}'

    resp = get_directions_tool_wrapper(json_input_string=query)

    print(resp)
