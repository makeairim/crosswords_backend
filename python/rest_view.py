from bottle import request, response,static_file,post, get,route,run,template
import os
import tempfile
import json
import ntpath
from sudoku import snap_sudoku
from random import randint

@get('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

debug=True

_names = set()
_names.add('SomeName')


def get_save_path_for_category():
    return 'D:\MEGASync\Semestr6\studio\crosswords_backend'


@get('/names')
def listing_handler():
    '''Handles name listing'''

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps({'names': list(_names)})


@route('/images/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root=get_save_path_for_category(), mimetype='image/png')


# @route('/upload', method='POST')
# def do_upload():
#     upload     = request.files.get('upload')
#     name, ext = os.path.splitext(upload.filename)
#     if ext not in ('.png','.jpg','.jpeg'):
#         return 'File extension not allowed.'
#
#     save_path = get_save_path_for_category()
#     upload.save(save_path) # appends upload.filename automatically
#
#     return 'OK'

@post('/upload')
def do_upload():
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png','.jpg','.jpeg'):
        return 'File extension not allowed.'

    save_path = get_save_path_for_category()
    # upload.filename = 'tmp1'+ext
    try:
        # tempFile = tempfile.NamedTemporaryFile(suffix=ext)
        # filename = 'tmp1'+ext
        # dir= os.path.dirname(tempFile.name)
        # head,tail = ntpath.split(tempFile.name)
        # print("dir= "+dir+"\n")
        # print(tail)
        # upload.filename=tail
        # tempFile.write(upload.file)
        dir =get_save_path_for_category()
        print(dir)
        filename = str(randint(1,10000))
        upload.filename = filename+ext
        print(upload.filename)
        upload.save(dir, True) # appends upload.filename automatically
        path = dir+"\\"+filename+ext
        result = snap_sudoku(path)
        # response.headers['Content-Type'] = 'application/json'
    except:
        return json.dumps({'result': 'Server error'})
    else:
        os.remove(path)
        return json.dumps({'path':path,'result':result})

@route('/')
def root():
    return static_file('form.html', root='.')


run(host='localhost', port=8080, debug=True)