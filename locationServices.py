import requests
import googlemaps
import streamlit as st
import ipinfo
from datetime import datetime
from ptcare import patientStates
import pyowm
import requests
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import json

def get_closest_hospitals(city, country):
    gmaps = googlemaps.Client(key='AIzaSyD-dm0fo4NtnjnFULpf1slbDSiu_rhAfhw')

    # Find the coordinates of the given city and country
    location = gmaps.geocode(f"{city}, {country}")[0]['geometry']['location']

    # Search for the 3 closest hospitals within 5000 meters of the given location
    places_result = gmaps.places_nearby(
        location,
        radius=5000,
        keyword='emergency'
    )

    # Extract the name and address of the 3 closest hospitals
    hospitals = []
    for place in places_result['results'][:3]:
        hospitals.append({
            'name': place['name'],
            'address': place['vicinity']
        })

    return hospitals

def get_closest_burn_centers(city, country):
    gmaps = googlemaps.Client(key='AIzaSyD-dm0fo4NtnjnFULpf1slbDSiu_rhAfhw')

    # Find the coordinates of the given city and country
    location = gmaps.geocode(f"{city}, {country}")[0]['geometry']['location']

    # Search for the 3 closest hospitals within 5000 meters of the given location
    places_result = gmaps.places_nearby(
        location,
        radius=100000,
        keyword='burn center'
    )

    # Extract the name and address of the 3 closest hospitals
    burn_centers = []
    for place in places_result['results'][:3]:
        burn_centers.append({
            'name': place['name'],
            'address': place['vicinity']
        })

    return burn_centers

def get_closest_trauma_centers(city, country):
    gmaps = googlemaps.Client(key='AIzaSyD-dm0fo4NtnjnFULpf1slbDSiu_rhAfhw')

    # Find the coordinates of the given city and country
    location = gmaps.geocode(f"{city}, {country}")[0]['geometry']['location']

    # Search for the 3 closest hospitals within 5000 meters of the given location
    places_result = gmaps.places_nearby(
        location,
        radius=100000,
        keyword='trauma center'
    )

    # Extract the name and address of the 3 closest hospitals
    trauma_centers = []
    for place in places_result['results'][:3]:
        trauma_centers.append({
            'name': place['name'],
            'address': place['vicinity']
        })

    return trauma_centers

def get_closest_stroke_centers(city, country):
    gmaps = googlemaps.Client(key='AIzaSyD-dm0fo4NtnjnFULpf1slbDSiu_rhAfhw')

    # Find the coordinates of the given city and country
    location = gmaps.geocode(f"{city}, {country}")[0]['geometry']['location']

    # Search for the 3 closest hospitals within 5000 meters of the given location
    places_result = gmaps.places_nearby(
        location,
        radius=100000,
        keyword='stroke center'
    )

    # Extract the name and address of the 3 closest hospitals
    stroke_centers = []
    for place in places_result['results'][:3]:
        stroke_centers.append({
            'name': place['name'],
            'address': place['vicinity']
        })

    return stroke_centers

def get_closest_cardiac_centers(city, country):
    gmaps = googlemaps.Client(key='AIzaSyD-dm0fo4NtnjnFULpf1slbDSiu_rhAfhw')

    # Find the coordinates of the given city and country
    location = gmaps.geocode(f"{city}, {country}")[0]['geometry']['location']

    # Search for the 3 closest hospitals within 5000 meters of the given location
    places_result = gmaps.places_nearby(
        location,
        radius=100000,
        keyword='cardiac center'
    )

    # Extract the name and address of the 3 closest hospitals
    cardiac_centers = []
    for place in places_result['results'][:3]:
        cardiac_centers.append({
            'name': place['name'],
            'address': place['vicinity']
        })

    return cardiac_centers

def get_location(ip_address):
    access_token = "5eddd8f1cfea71" 
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip_address)
    city = details.city
    country = details.country_name
    ret = [city, country]
    return ret


def get_ip_address():
    response = requests.get("https://api.ipify.org?format=json")
    ip_address = response.json()["ip"]
    return ip_address

def getLocationType(location, city, country):
    if(location == 'hospital'):
        return get_closest_hospitals(city, country)
    if(location == 'burn center'):
        return get_closest_burn_centers(city, country)
    if(location == 'trauma center'):
        return get_closest_trauma_centers(city, country)
    if(location == 'stroke center'):
        return get_closest_stroke_centers(city, country)
    if(location == 'cardiac center'):
        return get_closest_cardiac_centers(city, country)
    
def getRecDest(vitals, traumas):
    patient_states = patientStates(vitals)

    #initialize the functions storage of vitals given from the vitals list in the parameter
    gcs = int(vitals[0]) if vitals[0] != "" and vitals[0].isdigit() else None
    pulse = int(vitals[1]) if vitals[1] != "" and vitals[1].isdigit() else None
    resp_rate = int(vitals[2]) if vitals[2] != ""  and vitals[2].isdigit() else None
    pulse_ox = int(vitals[3]) if vitals[3] != "" and vitals[3].isdigit() else None
    breath_sounds = vitals[4].lower()
    blood_pressure = int(vitals[5].split('/')[0]) if vitals[5] != ""  and vitals[5].split('/')[0].isdigit() else None
    pupils = vitals[6].lower() + vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    skin_condition = vitals[7].lower() + vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    extra_notes = vitals[8].lower() + vitals[9].lower() + vitals[10].lower()
    avpu = vitals[11].lower()
    avpu_int = 16

    if('alert' in avpu):
        avpu_int = 15
    if('verbal' in avpu):
        avpu_int = 14
    if('pain' in avpu):
        avpu_int = 10
    if('unresponsive' in avpu):
        avpu_int = 3
    gcs = min(avpu_int, gcs) if gcs is not None else None
    if (avpu_int != 16 and gcs is None):
        gcs = avpu_int

    if(pulse is not None):
        if(pulse < 30):
            return 'hospital'
    if(resp_rate is not None):
        if(resp_rate < 10):
            return 'hospital'
    if(extra_notes is not None):
        if('cincin' in extra_notes or 'droop' in extra_notes or 'slur' in extra_notes or 'drift' in extra_notes):
            return 'stroke center'
    if(len(traumas) > 0):
        if('1st Degree Burn' in traumas or '2nd Degree Burn' in traumas or  '3rd Degree Burn' in traumas):
            return 'burn center'
        return 'trauma center'
    if(gcs is not None):
        if(gcs < 15):
            return 'hospital'
    if(pulse is not None):
        if(pulse < 60 or pulse > 100):
            return 'hospital'
    if(resp_rate is not None):
        if(resp_rate > 20 or resp_rate < 12):
            return 'hospital'
    if(pulse_ox is not None):
        if(pulse_ox < 95):
            return 'hospital'
    if(breath_sounds != ''):
        if(not('clear' in breath_sounds or 'healthy' in breath_sounds or 'vesicular' in breath_sounds)):
            return 'hospital'
    if(blood_pressure is not None):
        if(blood_pressure < 100 or blood_pressure > 160):
            return 'hospital'
    if(pupils is not None):
        if('pinpoint' in pupils):
            return 'hospital'
    if(skin_condition is not None):
        if('red' in skin_condition or 'flushed' in skin_condition or 'pale' in skin_condition or 'clammy' in skin_condition or 'diaphor' in skin_condition or 'cyan' in skin_condition or 'urtic' in skin_condition or 'rash' in skin_condition):
            return 'hospital'
    if(extra_notes is not None):
        if('chest' in extra_notes or 'diab' in extra_notes or 'angin' in extra_notes):
            return 'hospital'
    return ''

def rearrange_places(places, dest):
    if (dest == '' or dest == 'hospital'):
        return places

    if(dest == 'burn center'):
        places[0] = 'Burn Centers'
        places[1] = 'Hospitals'
    if(dest == 'trauma center'):
        places[0] = 'Trauma Centers'
        places[2] = 'Hospitals'
    if(dest == 'stroke center'):
        places[0] = 'Stroke Centers'
        places[3] = 'Hospitals'
    if(dest == 'cardiac center'):
        places[0] = 'Cardiac Centers'
        places[4] = 'Hospitals'

def get_weather(city: str, country: str) -> str:
    api_key = 'ab4b1f582a4a6a7a6284f2a40347570a' 
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    query = f'{city},{country}'
    params = {'q': query, 'appid': api_key, 'units': 'imperial'}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f'{temp}°F with {description}.'
    else:
        return 'Could not retrieve weather data.'


def get_city_country(latitude, longitude):
    gmaps = googlemaps.Client(key='AIzaSyD-dm0fo4NtnjnFULpf1slbDSiu_rhAfhw')
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))

    city = None
    country = None

    for component in reverse_geocode_result[0]['address_components']:
        if 'locality' in component['types']:
            city = component['long_name']
        if 'country' in component['types']:
            country = component['long_name']

        if city and country:
            break

    if city and country:
        return [city, country]
    else:
        return None

def get_lat_lng(input_dict):
    coords = input_dict.get('coords', {})

    latitude = coords.get('latitude')
    longitude = coords.get('longitude')

    if latitude is not None and longitude is not None:
        return [latitude, longitude]
    else:
        return None

def get_location():
    loc = get_geolocation()
    location = get_lat_lng(loc)
    location_city_country = get_city_country(location[0], location[1])
    return location_city_country

