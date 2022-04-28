import psycopg2
import keyring


class PostgisInterface:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect_db(self, user, dbname):
        try:
            self.connection = psycopg2.connect(dbname=dbname, user=user, password=keyring.get_password(dbname, user))
            self.cursor = self.connection.cursor()
            print(self.connection.get_dsn_parameters(), '\n')
            self.cursor.execute('SELECT version();')
            record = self.cursor.fetchone()
            print('You are connected to' + str(record))

        except (Exception, psycopg2.Error) as error:
            print('Error while connecting to PostgreSQL' + str(error))
            self.cursor = None

    def modify_db(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        pass

    def query_db(self, query):
        self.cursor.execute(query)
        record = self.cursor.fetchall()

        return record
