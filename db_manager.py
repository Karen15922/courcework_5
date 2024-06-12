import requests
import psycopg2

def create_database(dbname, user, password, host, port):
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cur = conn.cursor()

    try:
          # Создание таблиц employers и vacancies
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                employer_id INTEGER,
                title VARCHAR(255),
                salary VARCHAR(50),
                url TEXT,
                FOREIGN KEY (employer_id) REFERENCES employers (id) ON DELETE CASCADE
            )
        """)
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных и таблиц: {e}")
    finally:
        cur.close()
        conn.close()

class DBManager:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='6276703zx',
        host= '127.0.0.1',
        port= '5432'
)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute("SELECT name, COUNT(id) FROM employers  JOIN vacancies  ON id = employer_id GROUP BY name")
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute("SELECT name, title, salary, url FROM employers  JOIN vacancies  ON id = employer_id")
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute("SELECT AVG(salary::integer) FROM employers  JOIN vacancies  ON id = employer_id")
        return self.cur.fetchall()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute("SELECT name, title, salary, url FROM employers  JOIN vacancies  ON id = employer_id WHERE salary > %s", (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute("SELECT name, title, salary, url FROM employers  JOIN vacancies  ON id = employer_id WHERE to_tsvector(title) @@ to_tsquery(%s)", (keyword,))
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()