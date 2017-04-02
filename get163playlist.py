import requests as rq
import sys
import json
import db

def rep(s):
    s = s.replace("'","\\\'")
    s = s.replace('"',"\\\'")
    return s

class song:
    def __init__(self,name,artist,mp3,pic):
        self.title = rep(name)
        self.singer = rep(artist)
        self.source = rep(mp3)
        self.pic = rep(pic)
    def __str__(self):
        return self.title


def getSongs(id):
    url = 'http://music.163.com/api/playlist/detail?id='
    rp = rq.get(url+id)
    tracks = json.loads(rp.text)['result']['tracks']

    songs = []
    for item in tracks:
        name = item['name']
        artist = item['artists'][0]['name']
        mp3 = item['mp3Url']
        pic = item['album']['picUrl']
        songs.append(song(name,artist,mp3,pic))
    
    fail_list = []
    for item in songs:
        pic_rep = rq.get(item.pic)
        source_rep = rq.get(item.source)
        print('请求歌曲:%s' %item.title)
        if (pic_rep.status_code == 200 and source_rep.status_code == 200):
            print('成功下载!')
            f = open('pic/%s-%s.jpg' %(item.title.replace(' ',''),item.singer.replace(' ','')),'wb')
            f.write(pic_rep.content)
            f.close()
            f = open('source/%s-%s.mp3' %(item.title.replace(' ',''),item.singer.replace(' ','')),'wb')
            f.write(source_rep.content)
            f.close()
            music = {'title':item.title,'singer':item.singer,'source':item.title.replace(' ','') + '-' + item.singer.replace(' ','') + '.mp3','pic':item.title.replace(' ','') + '-' + item.singer.replace(' ','') + '.jpg'}
            db.insertData(music)
            print('成功保存！\n')
        else:
            print('下载失败!\n')
            fail_list.append(item.title)

    print('请求结束！')
    print('共请求%d首歌曲，失败下载%d首歌曲,失败下载歌曲为:' %(len(songs),len(fail_list)))
    print(fail_list)
    print('\n')

if __name__ == '__main__':
    ids = sys.argv[1:]
    for id in ids:
        getSongs(id)
