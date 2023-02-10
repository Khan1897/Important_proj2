import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://umma.ru/perevod-korana/'

data = requests.get(url).text

soup = bs(data, 'html.parser')

links = soup.find('main', {'id': 'quran'}).find_all('a')

links = [i['href'] for i in links]

print(links[4:])

url2 = 'https://umma.ru'


def getting_ayts(x):
    ayat_url = url2 + x
    sura1 = requests.get(ayat_url).text
    sura = bs(sura1, 'html.parser')

    alla = (sura.find('article', 'u_quran-sura__article').find_all('div', 'u_quran-ajat'))

    final = [i.find('div', 'u_quran-ajat__translate').find('p').text for i in alla]
    return final


z = []
for i in links[4:]:
    print(i)
    z.append(getting_ayts(i))


def getting_ids(x):
    final = []
    ayat_url = url2 + x
    sura1 = requests.get(ayat_url).text
    sura = bs(sura1, 'html.parser')

    alla = (sura.find('article', 'u_quran-sura__article').find_all('div'))

    for i in alla:
        try:
            final.append(i['id'])
        except Exception:
            pass
    return final


ids_of_ayts = []
for i in links[4:]:
    print(i)
    ids_of_ayts.append(getting_ids(i))

dict1 = {}

for i in range(len(ids_of_ayts)):
    ids_of_ayts[i] = list(map(lambda x: x.split('-'), ids_of_ayts[i]))

for i in range(len(ids_of_ayts)):
    for j in range(len(ids_of_ayts[i])):
        if ids_of_ayts[i][j] == ids_of_ayts[i][-1]:
            continue
        elif ids_of_ayts[i][j] != ids_of_ayts[i][-1]:
            if int(ids_of_ayts[i][j][-1]) - int(ids_of_ayts[i][j + 1][-1]) != -1:
                ids_of_ayts[i][j][-1] += '-' + str(int(ids_of_ayts[i][j + 1][-1]) - 1)
            else:
                continue

ids_of_ayts[-1][-1][-1] = '1-6'
ids_of_ayts[-2][-1][-1] = '1-5'
ids_of_ayts[-3][-1][-1] = '1-4'
ids_of_ayts[-4][-1][-1] = '1-5'
ids_of_ayts[-5][-1][-1] = '1-3'
ids_of_ayts[-6][-1][-1] = '1-6'
ids_of_ayts[-7][-1][-1] = '1-3'
ids_of_ayts[-9][-1][-1] = '1-4'
ids_of_ayts[-10][-1][-1] = '1-3'
ids_of_ayts[-12][-1][-1] = '1-3'

number_of_indexes = []
for i in range(len(ids_of_ayts)):
    number_of_ayts_in_sura = [str(i + 1)] * len(ids_of_ayts[i])
    number_of_indexes.extend(number_of_ayts_in_sura)

ordi_num_of_ayt = [j[-1] for i in ids_of_ayts for j in i]

all_ayts = [j for i in z for j in i]

dic1 = {'Sura': number_of_indexes, 'Ayt': ordi_num_of_ayt, 'Rus_Trans': all_ayts}

final_version = pd.DataFrame.from_dict(dic1)

all_ayts_only_lett1 = [i.translate(str.maketrans('', '', string.punctuation)) for i in all_ayts]

all_ayts_only_lett = [(i.lower()).replace(' ', '|') for i in all_ayts_only_lett1]

final_version['letters'] = all_ayts_only_lett