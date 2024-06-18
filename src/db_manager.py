import psycopg2
from prettytable import PrettyTable

class DBManager:
    def __init__(self, kwargs):
        self.__dict__.update(kwargs)

        self.conn = psycopg2.connect(
            dbname = self.dbname,
            user = self.user,
            password = self.password, 
            host = self.host,
            port = self.port
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute("SELECT name, COUNT(id) FROM employers  JOIN vacancies  ON id = employer_id GROUP BY name")
        table = PrettyTable()
        table.field_names = ['companies', 'vacancy_quantity']
        table.add_rows(self.cur.fetchall())
        print(table)

    def get_all_vacancies(self):
        self.cur.execute("SELECT name, title, salary, url FROM employers  JOIN vacancies  ON id = employer_id")
        table = PrettyTable()
        table.field_names = ['name', 'title', 'salary', 'url']
        table.add_rows(self.cur.fetchall())
        print(table)

    def get_avg_salary(self):
        self.cur.execute("SELECT AVG(salary::integer) FROM employers  JOIN vacancies  ON id = employer_id")
        table = PrettyTable()
        table.field_names = ['avg_salary']
        table.add_rows(self.cur.fetchall())
        print(table)

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute("SELECT name, title, salary, url FROM employers  JOIN vacancies  ON employers.id = vacancies.employer_id WHERE salary > (SELECT AVG(salary) FROM vacancies);")
        table = PrettyTable()
        table.field_names = ['name', 'title', 'salary', 'url']
        table.add_rows(self.cur.fetchall())
        print(table)

    def get_vacancies_with_keyword(self):
        keyword = input('Введи поисковой запрос:\n')
        self.cur.execute(f"SELECT name, title, salary, url FROM employers  JOIN vacancies  ON employers.id = vacancies.employer_id WHERE vacancies.title LIKE('%{keyword}%')")
        table = PrettyTable()
        table.field_names = ['name', 'title', 'salary', 'url']
        table.add_rows(self.cur.fetchall())
        print(table)

    def close(self):
        self.cur.close()
        self.conn.close()

