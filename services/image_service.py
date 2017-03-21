import os
from PIL import Image

# do celow testowych sciezki moga byc zaprute
#  todo przeniesc sciezki do plikow do pliku konfiguracyjnego, np. serwis zwracajacy sciezke
#  todo c.d. sciezka moze siedziec w plik. konfig. zaleznym od releasu aplikacji np. z argumentem dev serwer startuje z plikiem konfiguracyjnym app-dev, a z arg. prod z plikiem app-prod
def get_test_image_path():
    dir_path = os.path.dirname('D:\MEGASync\Semestr6\studio\.')
    img_path = os.path.join(dir_path, 'hat.jpg')
    return img_path

# todo jesli zamierzamy zapisywac zdjecia uzytkownika to nalezy dodac serwis do obslugi IO i prosta baze danych
def get_path_to_save():
    dir_path = os.path.dirname('D:\MEGASync\Semestr6\studio\.')
    img_path = os.path.join(dir_path, 'hatRCV.jpg')
    return img_path

# todo po wyslaniu jesli nie zapisujemy to powinnismy usuwac
def save_image(bytes):
    img_path=get_path_to_save()
    Image.open(bytes).save(img_path)
    return img_path


def get_image(path):
    return Image.open(path)