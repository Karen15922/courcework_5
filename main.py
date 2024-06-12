from src.db_manager import create_database, DBManager
from src.utils import get_vacancies
dbname='postgres'
user='postgres'
password='6276703zx'
host='localhost'
port='5432'
data = get_vacancies()

create_database(dbname, user, password, host, port, data)

db_manager = DBManager(dbname, user, password, host, port)


print(data.get('companies'))

