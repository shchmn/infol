from bs4 import BeautifulSoup as bs
import requests
import json
from pprint import pprint

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

vac = input('Кем хотите стать? ')
base_url = 'https://hh.ru'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
url = base_url + f'/search/vacancy?text={vac}&'


response = requests.get(url, headers=headers)
dom = bs(response.text, 'html.parser')
vacancies = dom.find_all('div', {'class': 'vacancy-serp-item-body'})


def max_num():
    mn = 0
    for i in dom.find_all('a', {'data-qa': 'pager-page'}):
        mn = list(i.strings)[0].split(' ')[-1]
    return mn


max_page = int(max_num())


def write_to_db(vac):
    client = MongoClient('127.0.0.1', 27017)
    db = client['hh']
    vacancy = db.hh
    if vacancy.find_one({'link': vac['link']}):
        print(f'Такое уже есть {vac["link"]}')
    else:
        vacancy.insert_one(vac)
        print(f'Новая вакансия {vac["link"]}')


def data_collect(pages, to_write=True):
    vacancies_list = []
    for p in range(pages):
        url_n = f'https://hh.ru/search/vacancy?text={vac}&page={p}'
        response_n = requests.get(url_n, headers=headers)
        dom_n = bs(response_n.text, 'html.parser')
        vacancies_n = dom_n.find_all('div', {'class': 'vacancy-serp-item-body'})
        for vacancy in vacancies_n:
            vacancy_data = {}
            vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
            vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text.strip()
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            vacancy_salary_data = {'min': '', 'max': '', 'currency': ''}
            if vacancy_salary is None:
                vacancy_salary_data['min'] = 'None'
                vacancy_salary_data['max'] = 'None'
                vacancy_salary_data['currency'] = 'None'
            else:
                vacancy_salary = vacancy_salary.text.replace('\u202f', '').split()
                if 'от' in vacancy_salary:
                    vacancy_salary_data['min'] = int(vacancy_salary[1])
                    vacancy_salary_data['max'] = 'None'
                    vacancy_salary_data['currency'] = vacancy_salary[2]
                elif 'до' in vacancy_salary:
                    vacancy_salary_data['min'] = 'None'
                    vacancy_salary_data['max'] = int(vacancy_salary[1])
                    vacancy_salary_data['currency'] = vacancy_salary[2]
                elif 'от' and 'до' not in vacancy_salary:
                    vacancy_salary_data['min'] = int(vacancy_salary[0])
                    vacancy_salary_data['max'] = int(vacancy_salary[2])
                    vacancy_salary_data['currency'] = vacancy_salary[3]
            vacancy_data['name'] = vacancy_name
            vacancy_data['link'] = vacancy_link
            vacancy_data['salary'] = vacancy_salary_data

            if to_write:
                write_to_db(vacancy_data)
            vacancies_list.append(vacancy_data)
        return vacancies_list



pprint(data_collect(max_page))


