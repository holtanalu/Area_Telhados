from PIL import Image
import os


lista_arquivos = os.listdir("img_hosp")

for img in lista_arquivos:

    imagem = Image.open(f"img_hosp/{img}")
    imagem.save(f"img_trein/{img.replace('png', 'gif')}")
