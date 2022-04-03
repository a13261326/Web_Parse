
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json

vacancies_list = []
profession = input('Введите ключеаое слово профессии:')
pages_total = input('Сколько страниц вывести?')
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
        vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
        vacancy_name = vacancy.find('span', {'class': 'resume-search-item__name'}).getText()
        vacancy_compensation = vacancy.find('span', {'class': 'bloko-header-section-3'})
        vacancy_company_link = vacancy.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'})['href']
        response2 = requests.get(base_url + vacancy_company_link, headers=headers)
        dom2 = bs(response2.text, 'html.parser')
        company_link = dom2.find('a', {'rel': 'noopener noreferrer nofollow noindex'})
        if vacancy_compensation:
            vacancy_compensation = vacancy_compensation.getText().replace('\u202f', ' ').replace(' ', ' ')
        else:
            vacancy_compensation = None
        if company_link:
            company_link = dom2.find('a', {'rel': 'noopener noreferrer nofollow noindex'})['href']
        else:
            company_link = None

        vacancy_data['salary'] = vacancy_compensation
        vacancy_data['link'] = vacancy_link
        vacancy_data['name'] = vacancy_name
        vacancy_data['company_site'] = company_link

        vacancies_list.append(vacancy_data)

        vacancy_compensation = ''
        vacancy_link = ''
        vacancy_name = ''
        company_link = ''
        print('--'*page*10)

with open("jobs.json", 'w') as fout:
    json_dumps_str = json.dumps(vacancies_list, indent=4,ensure_ascii=False)
    print(json_dumps_str, file=fout)



pprint(vacancies_list)
