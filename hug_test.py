import hug
import os
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


@hug.get('/getgif', output=hug.output_format.image('jpeg'))
def get():
    dir_path = os.path.dirname('D:\MEGASync\Semestr6\studio\.')
    img_path = os.path.join(dir_path, 'hat.jpg')
    img = Image.open(img_path)
    return img


if __name__ == '__main__':
    happy_birthday.interface.cli()
