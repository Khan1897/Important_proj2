import pandas as pd
import telebot
import keys
from nltk.stem.snowball import SnowballStemmer
import requests
from bs4 import BeautifulSoup

stemmer = SnowballStemmer("russian")

print('Bot started...')
API_KEY = keys.token

bot = telebot.TeleBot(API_KEY)

url = 'https://text.ru/synonym/'

def find_synonims(word: str):

    syn = requests.get(url + word).text
    soup = BeautifulSoup(syn, 'html.parser')
    table = soup.find('table', {'id': 'table_list_synonym'}).find_all('a')
    table = list(filter(lambda x: x.isalpha(),[i.text for i in table]))

    return table




@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Ассаламу Алейкум! Опишите одним словом интересующую Вас тему и, через пробел, количество аятов, которые Вы хотели бы видеть (к примеру, Милость 5)')

@bot.message_handler(func=lambda msg: True)
def get_ayts(message):
    see = message.text
    list_of_inf = see.split()
    if len(list_of_inf) == 2 and list_of_inf[0].isalpha() and list_of_inf[-1].isdigit():
        word0 = list_of_inf[0].lower()
        synonims = (find_synonims(word0))[:5]
        words = [stemmer.stem(word0)]
        for i in synonims:
            words.append(stemmer.stem(i.lower()))
        how_many = int(list_of_inf[-1])
    elif len(list_of_inf) != 2:
        bot.reply_to(message,'Вы ввели неправильное количество элементов. Нужно ввести только интересующее Вас слово и желанное Вами количество аятов. То есть, только два элемента')
        return
    elif list_of_inf[0].isalpha() != True:
        bot.reply_to(message, 'Введенное вами слово содержит какие-то символы, помимо букв')
        return
    elif list_of_inf[-1].isdigit() != True:
        bot.reply_to(message, 'Вы ввели не число, либо ввели его в неправильном формате. Число должне быть целым и больше нуля')
        return

    final_version = pd.read_csv(r"https://raw.githubusercontent.com/Khan1897/Quran_bot/main/Quran1.csv", encoding = 'utf-8', delimiter = ';')

    try:
        needed_ayts = pd.DataFrame({'Sura': [], 'Ayt': [], 'Rus_Trans': []})
        for word in words:
            ayts_you_get = final_version[final_version['letters'].str.contains(word)][['Sura','Ayt','Rus_Trans']]
            needed_ayts = pd.concat((needed_ayts,ayts_you_get.sample(frac = 1)), axis = 0)
        needed_ayts = needed_ayts.head(how_many)

        if (needed_ayts.shape)[0] != 0:

            for i,j,k in zip(list(needed_ayts['Sura']), list(needed_ayts['Ayt']), list(needed_ayts['Rus_Trans'])):
                a = (f"{i}:{j}\n{k}\n")
                bot.reply_to(message, a)
        else:
            bot.reply_to(message,'Не подобрано подходящего значения. Проверьте, правильно ли Вы написали слово или существует ли вообще написанное Вами слово')

    except Exception:
        bot.reply_to(message,'Не подобрано подходящего значения. Проверьте, правильно ли Вы написали слово или существует ли вообще написанное Вами слово')



if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)