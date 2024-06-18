import requests, os, click

import psycopg2

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
                salary = int(money.get('from'))
            else:
                salary = int(money.get('to'))
        
            vacancies.append([_id, com_id, name, salary, url_])
    return {'companies': companies, 'vacancies': vacancies}

def connection_details():
    dbname = input("Введите название базы данных: ")  
    user = input("Введите пользователя: ")
    password = input("Введите пароль: ")
    host = input("Введите хост: ")
    port = int(input("Введите порт: "))
    return {'dbname':dbname, 'user':user, 'password':password, 'host':host, 'port':port}


def create_table_and_fill_it(dbname, user, password, host, port, data):
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    vacancies = data.get('vacancies')
    companies = data.get('companies')


    try:
          # Создание таблиц employers и vacancies
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id INTEGER PRIMARY KEY NOT NULL,
                name VARCHAR(255)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INTEGER PRIMARY KEY NOT NULL,
                employer_id INTEGER,
                title VARCHAR(255),
                salary INTEGER,
                url TEXT,
                FOREIGN KEY (employer_id) REFERENCES employers(id)
            )
        """)
        cur.execute("TRUNCATE TABLE employers CASCADE;")
        for company in companies:
            cur.execute("INSERT INTO employers VALUES(%s, %s);", company)
        conn.commit()

        cur.execute("TRUNCATE TABLE vacancies CASCADE;")
        for vacancy in vacancies:
            cur.execute("INSERT INTO vacancies VALUES(%s, %s, %s, %s, %s);", vacancy)
        conn.commit()

    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных и таблиц: {e}")
    finally:
        cur.close()
        conn.close()
        
def default():
    print('unknown_input')


def what_do_you_want(db_manager):
    actions = [
            '1. Вывести список компаний и количество вакансий',
            '2. Вывести все вакансии',
            '3. Вывести среднюю зарплату',
            '4. Вывести вакансии с зарплатой выше средней',
            '5. Вывести вакансии по поисковому запросу',
            '6. Выход'
            ]
    commands = {
            '1': db_manager.get_companies_and_vacancies_count,
            '2': db_manager.get_all_vacancies,
            '3': db_manager.get_avg_salary,
            '4': db_manager.get_vacancies_with_higher_salary,
            '5': db_manager.get_vacancies_with_keyword,
            '6': exit}


    while True:
        try:
            os.system('clear')
            print('Доступны следующие действия:')
            for action in actions:
                print(action)
            user_select = input('выбери что-нибудь\n')
            commands.get(user_select, default)()
            click.pause()

        except ValueError:
            print('Можно только цмфры')

