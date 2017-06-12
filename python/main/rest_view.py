import base64
import json
from bottle import request, response, static_file, post, get, route, run, template
from random import randint

from backtrack import solveSudoku, print_grid
from solver import get_matrix


@get('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


debug = True

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

@get('/image/<filename>')
def do_download(filename):
    dir = get_save_path_for_category()
    ext = '.jpg'
    path = dir + "\\" + filename + ext
    f = open(path, 'rb');
    content = f.read();
    return content;


@post('/upload2')
def do_upload2():
    dir = get_save_path_for_category()
    print (dir)
    filename = str(randint(1, 10000))
    ext = '.jpg'
    # upload.filename = filename + ext
    # # print(upload.filename)
    # # upload.save(dir, True)  # appends upload.filename automatically
    path = dir + "\\" + filename + ext
    print(path)
    f = open(path, 'wb')
    f.write(base64.standard_b64decode(request.body.read()))
    f.close()
    matrix = get_matrix(path)
    (res, grid) = solveSudoku(matrix)
    if (res == True):
        print_grid(grid)
    if request.headers['Content-Type'] == 'application/json':
        return json.dumps({'result': 'octet stream1'})
    else:
        response.headers['Content-Type'] = 'Content-Type: application/json; charset=UTF-8'
        return json.dumps({'result': filename})


@post('/upload')
def do_upload():
    # upload = request.files.get('image')
    # name, ext = os.path.splitext(upload.filename)
    # if ext not in ('.png','.jpg','.jpeg'):
    #    return 'File extension not allowed.'
    # if request.headers['Content-Type'] == 'application/json':
    # return json.dumps({'result': 'octet stream1'})
    # else:
    # print(request.body)
    body = request.body.read()
    jsonObj = json.loads(body);
    # return json.dumps({'result': jsonObj['content']})
    # save_path = get_save_path_for_category()
    # upload.filename = 'tmp1'+ext
    # try:
    # tempFile = tempfile.NamedTemporaryFile(suffix=ext)
    # filename = 'tmp1'+ext
    # dir= os.path.dirname(tempFile.name)
    # head,tail = ntpath.split(tempFile.name)
    # print("dir= "+dir+"\n")
    # print(tail)
    # upload.filename=tail
    # tempFile.write(upload.file)
    dir = get_save_path_for_category()
    print(dir)
    filename = str(randint(1, 10000))
    ext = '.jpg'
    # upload.filename = filename + ext
    # # print(upload.filename)
    # # upload.save(dir, True)  # appends upload.filename automatically
    path = dir + "\\" + filename + ext
    print(path)
    f = open(path, 'wb')
    f.write(jsonObj['content'])
    f.close()
    result = path
    # result = snap_sudoku(path)
    #    result='ss'
    # response.headers['Content-Type'] = 'application/json'
    # except IOError as e:
    #   print("I/O error({0}): {1}".format(e.errno, e.strerror))
    #  return json.dumps({'result': 'Cannot solve sudoku'})
    # else:
    # os.remove(path)
    return json.dumps({'result': result})


@route('/')
def root():
    return static_file('form.html', root='.')


run(host='localhost', port=8080, debug=True)
