import io
import os

import hug
from PIL import Image

# @hug.cli()
# @hug.get(examples='name=Timothy&age=26')
# @hug.local()
# def happy_birthday(name: hug.types.text, age: hug.types.number, hug_timer=3):
#     """Says happy birthday to a user"""
#     return {'message': 'Happy {0} Birthday {1}!'.format(age, name),
#             'took': float(hug_timer)}
api = hug.get(on_invalid=hug.redirect.not_found)


@api.urls('/do-math', examples='number_1=1&number_2=2')
def math(number_1: hug.types.number, number_2: hug.types.number):
    return number_1 + number_2


@api
def happy_birthday(name, age: hug.types.number):
    """Says happy birthday to a user"""
    return "Happy {age} Birthday {name}!".format(**locals)


@hug.get('/api/image', output=hug.output_format.image('jpeg'))
def get():
    dir_path = os.path.dirname('D:\MEGASync\Semestr6\studio\.')
    img_path = os.path.join(dir_path, 'hat.jpg')
    img = Image.open(img_path)
    return img


@hug.post('/api/image', output=hug.output_format.image('jpeg'))
def post(body=None):
    dir_path = os.path.dirname('D:\MEGASync\Semestr6\studio\.')
    img_path = os.path.join(dir_path, 'hatRCV.jpg')
    Image.open(io.BytesIO(body.read())).save(img_path);
    resp = 'OK'
    return resp


if __name__ == '__main__':
    happy_birthday.interface.cli()
