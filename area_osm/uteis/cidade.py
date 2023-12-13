from geopy import Nominatim

lat = -23.8429362
lon = -46.1396987

lugar = Nominatim(user_agent="myGeocoder").reverse(f"{lat}, {lon}")

print(lugar.raw)
