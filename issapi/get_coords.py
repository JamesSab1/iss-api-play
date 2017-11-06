from django.shortcuts import render
import requests, json, geopy
from geopy.geocoders import Nominatim


def get_coords(address):
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    lat = location.latitude
    lon = location.longitude
    print(lat, lon)



