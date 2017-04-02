from db import *
import bottle

app = application = bottle.Bottle()

@app.route('/')
def index():
    return bottle.template('index.html')

@app.route('/static/<fn>')
def static(fn):
    return bottle.static_file(fn,root='./')


def simple(x):
    res = []
    for i in x:
        res.append([i[0],i[1],i[2]])
    return res

def simple2(x):
    res = []
    for i in x:
        res.append([i[1],i[2],i[3],i[4]])
    return res

@app.route('/getSongs')
def getSongs():
    data = getData('songs')
    data = simple(data)
    return {'songs': data}

@app.route('/getSong/<id>')
def getSong(id):
    data = getData('songs',id)
    data = simple2(data)
    return {'song': data}

@app.route('/get/source/<mp3>')
def get(mp3):
    print(mp3)
    return bottle.static_file(mp3,root='resource/songs',mimetype='audio/mpeg')

@app.route('/get/pic/<pic>')
def get(pic):
    print(pic)
    return bottle.static_file(pic,root='resource/pics',mimetype='image/jpeg')
