import io

import hug
from PIL import Image

from services import image_service

# @hug.cli()
# @hug.get(examples='name=Timothy&age=26')
# @hug.local()
# def happy_birthday(name: hug.types.text, age: hug.types.number, hug_timer=3):
#     """Says happy birthday to a user"""
#     return {'message': 'Happy {0} Birthday {1}!'.format(age, name),
#             'took': float(hug_timer)}

api = hug.get(on_invalid=hug.redirect.not_found)

# start region test
@api.urls('/do-math', examples='number_1=1&number_2=2')
def math(number_1: hug.types.number, number_2: hug.types.number):
    return number_1 + number_2


@api
def happy_birthday(name, age: hug.types.number):
    """Says happy birthday to a user"""
    return "Happy {age} Birthday {name}!".format(**locals)
# end region test

@hug.get('/api/image', output=hug.output_format.image('jpeg'))
def get():
    img_path = image_service.get_test_image_path()
    img = image_service.get_image(img_path);
    return img


@hug.post('/api/image', output=hug.output_format.image('jpeg'))
def post(body=None):
    image_service.save_image(io.BytesIO(body.read()))
    resp = 'OK'
    return resp

# todo obsluga bledow, do celow testowych i dev bedzie najlepiej zrobic prosty serwis albo podpiac biblitoeke do zapisywania logow,usprawni to dalsza prace i nie bedzie sie szukac bledow nie wiadomo w ktorej czesci
# todo c.d. mozna rozdzielic zapisywanie zwyklych logow, wszystkich i bledow
if __name__ == '__main__':
    happy_birthday.interface.cli()
