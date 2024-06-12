import requests
import os 

def get_vacancies():
    url = 'https://api.hh.ru/'
    params = {'page': 0, 'per_page':100, 'only_with_salary': True}
    vacancies = []
    companies = []

    list_companies = ['1740', '39305', '78638', '3529', '2748', '4496', '1049556', '4352', '2180', '58320']
    for company_id in list_companies:
        response = requests.get(f"{url}employers/{company_id}",params=params)
        founded_company = response.json()

        company_vacancies = founded_company.get('vacancies_url')
        companies.append([int(founded_company.get('id')), founded_company.get('name')])
        response = requests.get(company_vacancies, params=params)
        data = response.json()
        list_vacancy = data['items']

        for vacancy in list_vacancy:
            com_id = int(vacancy.get('employer').get('id'))
            name = vacancy.get('name')
            _id  = int(vacancy.get('id'))
            money = vacancy.get('salary')
            url_ = vacancy.get('url')
            if money.get('from') != None:
                salary = money.get('from')
            else:
                salary = money.get('to')       
        
            vacancies.append([_id, com_id, name, salary, url_])
    return {'companies': companies, 'vacancies': vacancies}




