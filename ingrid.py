# -*- coding: utf-8 -*-
import requests
import sqlite3
import Levenshtein
from bs4 import BeautifulSoup


def ingrid_search(req):
    mas = []
    connect = sqlite3.connect('list.db')
    cur = connect.cursor()
    for value in cur.execute("""select rus_name from ingrid;"""):
        if req.lower() in value[0].lower():
            mas.append([0, value[0]])
        else:
            r = Levenshtein.distance(value[0].lower(), req.lower())
            mas.append([r, value[0]])
    mas.sort(key=lambda a: a[0])
    mas5 = []
    for i in range(5):
        mas5.append(mas[i][1])
    return mas5


def recipes(ingrid_list):
    connect = sqlite3.connect('list.db')
    cur = connect.cursor()
    url = 'https://povar.ru/master/'
    for ingrid in ingrid_list:
        cur.execute(f"""select eng_name from ingrid where rus_name='{ingrid}';""")
        url_eng = cur.fetchone()[0]
        url = url + url_eng + '-'
    url = url[:-1] + '/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features='html.parser')
    all_rec = soup.findAll('div', class_='recipe')
    count = 0
    mas = []
    site = 'https://povar.ru'
    for i in all_rec:
        name = i.find('a', class_='listRecipieTitle').text
        link = i.find('a', class_='listRecipieTitle').get('href')
        link = site + link
        mas.append([name, link])
        count += 1
        if count > 4:
            break
    return mas


def recommend(ingrid_list):
    mas = []
    d = len(ingrid_list)
    if d > 5:
        d = 5

    for i in range(d):
        mas = recipes(ingrid_list[:d-i])
        if len(mas) != 0:
            break
    return mas
