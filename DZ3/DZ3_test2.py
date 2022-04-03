from pymongo import MongoClient
from pprint import pprint


def salary(s=int):
    client = MongoClient('127.0.0.1', 27017)
    db = client['hh']
    professions = db.professions
    mylist = []
    # for doc in professions.find({'$or': [{'author': 'Peter2'}, {'age': {'$lte': 30}}]}):
    for doc in professions.find({'salary': {'$ne': None}}):
        min_salary = ''
        max_salary = ''
        USD = ''
        EUR = ''
        a = ''
        b = ''
        a = (doc['salary'].replace('–', '/').replace(' ', '').replace('до', '1-').replace('от', '').replace('руб.', ''))
        USD = a.find('USD')
        EUR = a.find('EUR')
        a = a.replace('/', ' ').replace('-', ' ').replace('USD', '').replace('EUR', '').split()
        b = len(list(a))
        if b == 2:
            min_salary = int(a[0])
            max_salary = int(a[1])
            if USD == 9:
                min_salary = min_salary * 84
                max_salary = max_salary * 84
            elif EUR == 9:
                min_salary = min_salary * 104
                max_salary = max_salary * 104
        elif b == 1:
            max_salary = int(a[0])
            if USD == True:
                max_salary = max_salary * 84
            elif EUR == True:
                min_salary = min_salary * 104
        if s <= max_salary and b == 2:
            mylist.append(doc)
        elif b == 1 and s <= max_salary:
            mylist.append(doc)

    pprint(mylist)


salary(300000)
