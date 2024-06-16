import psycopg2
class DBManager:
    def __init__(self, *args):
        self.dbname = None
        self.user = None
        self.password = None
        self.host = None
        self.port = None
        self.connection_details = [self.dbname, self.user, self.password, self.host, self.port]

        for num, value in enumerate(args):
            self.connection_details[num] = value
            
        self.conn = psycopg2.connect(
            dbname = self.dbname,
            name = self.user,
            password = self.password, 
            host = self.host,
            port = self.port
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