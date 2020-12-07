import os
try:
    import requests
    from requests.exceptions import HTTPError
except ImportError:
    instLib = input('''
             У вас не установлена библиотека requests.
             Данная библиотека необходима для работы приложения.
             Желаете начать усновку?
             Да/Нет
    ''')
    if instLib.lower() == 'да':
        os.system('pip install requests')
        os.system('cls')
else:
    raise SystemExit
import json


# источник данных
URL = 'http://jservice.io/api/random'


# запрос данных
def getResponse(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except (HTTPError, e):
        if e.code == 650:
            print('Ошибка соединения')
        elif e.code == 404:
            print('Ошибка стороны сервера')
        else:
            print('Ошибка получения данных')
    else:
        return json.loads(r.text)


# получение значений ключей
def getQuestion(response):
    return response[0]['question']


def getAnswer(response):
    return response[0]['answer']


def getValue(response):
    return response[0]['value']


def game(name, count):
    playerValue = 0

    maxValue = 0

    print(f'''
             Отлично, {name}! Викторина начинается!😈
             {name}, у тебя {playerValue} очков, достигни же максимума!
    ''')

    for i in range(count):
        response = getResponse(URL)
        question = getQuestion(response)
        answer = getAnswer(response)
        value = getValue(response)

        try:
            maxValue += value
        except:
            print('''
             Непредвиденная ошибка, вопрос не засчитывается 😢
            ''')

        # задача вопроса
        if i + 1 == count:
            playerAnswer = input(f'''
             Внимание! Это последний вопрос!
             Подготовься!
             Вопрос: "{question}"?
             Твой ответ:
            ''')
        else:
            playerAnswer = input(f'''
             {i + 1} вопрос!
             Итак: "{question}"?
             Твой ответ:
            ''')

        # сравнение результатов
        if answer.lower() != playerAnswer.lower():
            print(f'''
             Почти!
             Но правильный ответ: {answer}
             ''')
        else:
            playerValue += value
            print(f'''
             И это правильный ответ!
             Плюс {value} очков!
             Твой счет: {playerValue}
            ''')

    # вывод результата
    if playerValue < maxValue // 2:
        again = input(f'''
             Твой счет: {playerValue}...
             Главное не грусти, а бегом читать энциклопедию!
             Хочешь попробовать еще(Да или Нет)?
         ''')
    elif playerValue < maxValue:
        again = input(f'''
             Твой счет: {playerValue}!
             Это неплохой результат, но не предел!
             Хочешь попробовать еще(Да или Нет)?
         ''')
    else:
        again = input(f'''
             Твой счет: {playerValue}!
             Ты точно человек?! Или ты Савант, Мэрилин вос?
             Признавайся!
             Хочешь попробовать еще(Да или Нет)?
         ''')

    # запись результата в файл
    result = {
        'result': {
            'name': name,
            'score': playerValue,
            'max score': maxValue
        }
    }
    with open('results.txt', 'a') as f:
        json.dump(result, f)

    if again.lower() == 'да':
        countQuestions = 0
        while countQuestions < 1:
            try:
                countQuestions = int(input(f'''
             На какое количество вопросов
             ты хотел бы ответить?
             Введи число больше 0:'''))
            except:
                print('''
             Только числа!
                ''')
        os.system('cls')
        game(name, countQuestions)
    else:
        print('''
             Спасибо за игру!
        ''')
        # вызов закрытия программы
        raise SystemExit


def main():
    print(f'''
             Привет, это игра-викторина!
             В игре есть более чем 156 800 простых вопросов
             и ответов!
             Вопросы и ответы на английском языке!
             🤩🤩🤩
             \n
            ''')
    print(f'''
             Цель игры - набрать наибольшее количество баллов!
             Баллы сохраняются после каждой попытки,
             так что можно играть каждый день!
             🤓
             \n
    ''')
    playerName = input(f'''
             Как ты представишься?
             ''')
    countQuestions = 0
    while countQuestions < 1:
        try:
            countQuestions = int(input(f'''
             На какое количество вопросов
             ты хотел бы ответить?
             Введи число больше 0:'''))
        except:
            print('''
             Только числа!
            ''')
    os.system('cls')
    game(playerName, countQuestions)


if __name__ == '__main__':
    main()