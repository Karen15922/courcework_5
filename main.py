from src.db_manager import  DBManager
from src.utils import  connection_details, create_table_and_fill_it, get_vacancies, what_do_you_want

con_det = {'dbname': 'turbo_db',
            'user': 'turbo',
            'password': 'lkjsdf',
            'host': 'localhost',
            'port': 5432
            }

#connection_details = connection_details()
#connection_details['data'] = get_vacancies()


#create_table_and_fill_it(**connection_details)

#db_manager = DBManager(connection_details)



db_manager = DBManager(con_det)

what_do_you_want(db_manager)



