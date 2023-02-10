import pandas as pd
import keys
import telebot

print('Bot started...')
API_KEY = keys.token

bot = telebot.TeleBot(API_KEY)


def words_parts(word):
    driver = webdriver.Chrome()
    url_for_word = 'https://kartaslov.ru/%D1%80%D0%B0%D0%B7%D0%B1%D0%BE%D1%80-%D1%81%D0%BB%D0%BE%D0%B2%D0%B0-%D0%BF%D0%BE-%D1%81%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D1%83-%D0%BE%D0%BD%D0%BB%D0%B0%D0%B9%D0%BD'
    driver.get(url_for_word)
    sbox = driver.find_element(By.ID, 'queryBoxNew')
    sbox.send_keys(word)
    submit = driver.find_element(By.CLASS_NAME, 'v2-searchBox-submit-btn')
    submit.click()

    new_url = driver.current_url
    new_data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    parts = soup.find('table', 'morphemics-table-v2').find_all('td')
    parts = [i.text for i in parts]
    dic_parts = {j: i for i, j in zip(a[0::2], a[1::2])}

    return dic_parts

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Ассаламу Алейкум! Опишите одним словом интересующую Вас тему и, через пробел, количество аятов, которые Вы хотели бы видеть (к примеру, Милость 5)')

@bot.message_handler(func=lambda msg: True)
def get_ayts(message):
    see = message.text
    list_of_inf = see.split()
    if len(list_of_inf) == 2 and list_of_inf[0].isalpha() and list_of_inf[-1].isdigit():
        word = list_of_inf[0].lower()
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
        ayts_you_get = final_version[final_version['letters'].str.contains(word)][['Sura','Ayt','Rus_Trans']]
        needed_ayts = ayts_you_get.sample(frac = 1).head(how_many)

        for i,j,k in zip(list(needed_ayts['Sura']), list(needed_ayts['Ayt']), list(needed_ayts['Rus_Trans'])):
            a = (f"{i}:{j}\n{k}\n")
            bot.reply_to(message, a)
    except Exception:
        bot.reply_to(message,'Не подобрано подходящего значения. Проверьте, правильно ли Вы написали слово или существует ли вообще написанное Вами слово')



if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)