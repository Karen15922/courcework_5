from src.db_manager import  DBManager
from src.utils import  connection_details, create_table_and_fill_it, get_vacancies

dbname='postgres'
user='postgres'
password='6276703zx'
host='localhost'
port='5432'
data = get_vacancies()

connection_details = connection_details()

create_table_and_fill_it(dbname, user, password, host, port, data)

db_manager = DBManager(connection_details)