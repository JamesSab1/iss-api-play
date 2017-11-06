from django.shortcuts import render
import requests, json, geopy
from geopy.geocoders import Nominatim
from datetime import datetime
from django.http import Http404



##def get_coords(address):
##    geolocator = Nominatim()
##    location = geolocator.geocode(address)
##    lat = location.latitude
##    lon = location.longitude
##    return lat, lon
    
    


def index(request):
    #iss now
    status_code = requests.get("http://api.open-notify.org/iss-now.json")
    data = status_code.json()
    time = data['timestamp']
    nice_time = datetime.fromtimestamp(int(time)).strftime('%H:%M:%S')
    current_lat = data['iss_position']['latitude']
    current_lon = data['iss_position']['longitude']
        

    if request.method == 'POST':
        pass_address = request.POST['pass_address']
    else:
        pass_address = 'Birchwood, Warrington'
        
    geolocator = Nominatim()
    location = geolocator.geocode(pass_address)
    if location:
        lat = location.latitude
        lon = location.longitude
    else:
        raise Http404

    #get address from coords
    
    
    current_address = geolocator.reverse(current_lat+','+current_lon)
    iss_address = str(current_address.address)
    if iss_address == 'None':
        iss_address = 'an ocean'
    
    


    parameters = {"lat": lat, "lon": lon}
    #iss passing location
    iss_position_data = requests.get("http://api.open-notify.org/iss-pass.json",
                        params=parameters)
    iss_position = iss_position_data.content
    iss_position_passes = iss_position_data.json()
    passes = iss_position_passes['response']
    risetimes = [li['risetime'] for li in passes]
    nice_risetimes = []
    for time in risetimes:
        nice_risetime = datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
        nice_risetimes.append(nice_risetime)
    

    # astros data
    astros = requests.get("http://api.open-notify.org/astros.json")
    astros_data = astros.json()

    #people currently in space
    num_astros = astros_data["number"]
    name_astros = astros_data['people']


    name_list=[]
    for astro in name_astros:
        name_list.append(astro['name'])
    
        
    
    return render(request, 'issapi/index.html', {'status_code': status_code,
                                                 'iss_position':iss_position,
                                                 'num_astros':num_astros,
                                                 'name_astros':name_astros,
                                                 'name_list':name_list,
                                                 'nice_time':nice_time,
                                                 'iss_address':iss_address,
                                                 'nice_risetimes':nice_risetimes,
                                                 'pass_address':pass_address})



