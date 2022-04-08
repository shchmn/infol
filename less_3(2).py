from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['hh']
vacancy = db.hh

currency_dict = {1: 'руб.', 2: 'USD'}
while True:
    salary = input('Минимальная зарплата: ')
    currency = input('В какой валюте?: \n1 для USD, \n2 для руб.\n')
    try:
        salary = int(salary)
        currency = int(currency)
        if currency > 2 or currency < 1:
            print('Ошибка при вводе валюты')
            continue
        break
    except ValueError:
        print('Ошибка при вводе значения')


for doc in vacancy.find({'$or': [
    {'min_salary': {'$gte': salary}, 'max_salary': None, 'salary_currency': currency_dict[currency]},
    {'max_salary': {'$gte': salary}, 'salary_currency': currency_dict[currency]}
]}):
    pprint(doc)
