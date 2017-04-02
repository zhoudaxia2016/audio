import sqlite3
import os

def createDatabase():
    conn = sqlite3.connect('Songs.db')
    cu = conn.cursor()

    cu.execute('''create table songs
        (id integer primary key autoincrement,
        title char(30) not null,
        singer char(30),
        source char(30),
        pic char(30))''')
    conn.commit()
    conn.close()

def insertData(*args):
    conn = sqlite3.connect('Songs.db')
    cu = conn.cursor()
  
    for arg in args:
        sql = '''insert into songs(id,title,singer,source,pic)
            values(null,"%s","%s","%s","%s")'''%(arg['title'],arg['singer'],arg['source'],arg['pic'])
        cu.execute(sql)

    conn.commit()
    conn.close()

def showTable(n):
    conn = sqlite3.connect('Songs.db')
    cu = conn.cursor()
    cu.execute('select * from %s' %n)
    print(cu.fetchall())
    conn.close()

def getData(n,id=0):
    conn = sqlite3.connect('Songs.db')
    cu = conn.cursor()
    if id == 0:
        cu.execute('select * from %s' %n)
    else:
        cu.execute('select * from %s where id = %s' %(n,id))
    data = cu.fetchall()
    conn.close()
    return data


if __name__ == '__main__':
    createDatabase()
        
