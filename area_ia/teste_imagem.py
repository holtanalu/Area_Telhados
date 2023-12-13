from io import BytesIO
from PIL import Image
from urllib import request
from chave_api_static import API_KEY


url = f"http://maps.googleapis.com/maps/api/staticmap?center=-23.593291472341953,-46.561300593370376&size=250x250&zoom=\
        18&maptype=satellite&sensor=false&key={API_KEY}"

buffer = BytesIO(request.urlopen(url).read())
image = Image.open(buffer)

# Show Using PIL
image.show()
image.save("map11.png")
