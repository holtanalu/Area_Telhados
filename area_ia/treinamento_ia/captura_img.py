import time
from io import BytesIO
from PIL import Image
from urllib import request
from chave_api_static import API_KEY


coordenadas = open('tabelas_ia/coordenadas.txt', 'r')
lista = coordenadas.readlines()

for i in range(len(lista)):
    lat, lon = [float(x) for x in lista[i].split()]
    url = f"http://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&size=250x250&zoom=18&maptype=satellite&sensor=false&key={API_KEY}"

    buffer = BytesIO(request.urlopen(url).read())
    image = Image.open(buffer)

    # Show Using PIL
    # image.show()
    image.save(f"img_hosp/map{i}.png")
    print(i)
    time.sleep(1)
