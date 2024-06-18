from src.db_manager import  DBManager
from src.utils import  connection_details, create_table_and_fill_it, get_vacancies, what_do_you_want


connection_details = connection_details()
connection_details['data'] = get_vacancies()


create_table_and_fill_it(**connection_details)

db_manager = DBManager(connection_details)



db_manager = DBManager(connection_details)

what_do_you_want(db_manager)



