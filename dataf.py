
import sqlite3
from datetime import datetime as dt


def add(user_id, name, date):
    connect = sqlite3.connect('data.db')
    cur = connect.cursor()
    cur.execute(f"""insert into data values(
        {user_id},
        '{name}',
        '{date}'
            );""")
    connect.commit()


def check(user_id):
    connect = sqlite3.connect('data.db')
    cur = connect.cursor()
    s = ''
    for line in cur.execute(f"""select * from data where id = {user_id} """):
        s += 'Есть ' + line[1] + " который испортится "+line[2]+'. \n'
    if s == '':
        s = 'У вас ничего не добавлено'
    return s


def sooner(user_id):
    connect = sqlite3.connect('data.db')
    cur = connect.cursor()
    mas = []
    for line in cur.execute(f"""select * from data where id = {user_id} """):
        mas.append([dt.strptime(line[2], '%d.%m.%y'), line[1]])
    mas.sort(key=lambda d: d[0])
    mas5 = []
    count = 0
    for el in mas:
        mas5.append(el[1])
        if count > 4:
            break
    return mas5
