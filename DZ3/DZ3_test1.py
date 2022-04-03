import re
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient


client = MongoClient('127.0.0.1', 27017)
db = client['hh']
professions = db.professions
profession = input('Введите ключевое слово профессии:')
try:
    pages_total = int(input('Сколько страниц вывести:'))
except ValueError:
    print("Error! Это не число")
    quit()
base_url = 'https://hh.ru/'
for page in range(int(pages_total)):
    url = f'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&text={profession}&page={page}&hhtmFrom=vacancy_search_list'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}
    response = requests.get(url, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancies:
        vacancy_data = {}
        vacancy_link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
        vacancy_name = vacancy.find('span', {'class': 'resume-search-item__name'}).getText()
        vacancy_compensation = vacancy.find('span', {'class': 'bloko-header-section-3'})
        vacancy_company_link = vacancy.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'})['href']
        response2 = requests.get(base_url + vacancy_company_link, headers=headers)
        dom2 = bs(response2.text, 'html.parser')
        company_link = dom2.find('a', {'rel': 'noopener noreferrer nofollow noindex'})
        vacancy_id = re.search(r'\d+', vacancy_link)

        if vacancy_compensation:
            vacancy_compensation = vacancy_compensation.getText().replace('\u202f', ' ').replace(' ', ' ')
        else:
            vacancy_compensation = None
        if company_link:
            company_link = dom2.find('a', {'rel': 'noopener noreferrer nofollow noindex'})['href']
        else:
            company_link = None
        vacancy_data['_id'] = vacancy_id[0]
        vacancy_data['salary'] = vacancy_compensation
        vacancy_data['link'] = vacancy_link
        vacancy_data['name'] = vacancy_name
        vacancy_data['company_site'] = company_link

        try:
            professions.insert_one(vacancy_data)
        except DuplicateKeyError:
            print(f"Document with id = {vacancy_data['_id']} already exist")

        vacancy_id = ''
        vacancy_compensation = ''
        vacancy_link = ''
        vacancy_name = ''
        company_link = ''
        print('--' * page * 10)

result = list(professions.find({}))
pprint(result)
print(f'Всего записей {len(result)}')
