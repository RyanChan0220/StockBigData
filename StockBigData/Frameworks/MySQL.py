__author__ = 'Ryan'

import MySQLdb


class MySQL(object):
    __db_name = ""
    __con = None

    def __init__(self, db_name):
        self.__db_name = db_name

    def connect(self):
        try:
            self.__con = MySQLdb.connect(host='localhost', user='root',
                                         passwd='7758258', db=self.__db_name,
                                         port=3306)
        except MySQLdb.Error, e:
            print "Mysql connect error %d: %s" % (e.args[0], e.args[1])

    def close_connect(self):
        self.__con.close()

    def execute_statement(self, statement):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute(statement)
            cur.close()

    def execute_statement_with_ret(self, statement):
        data = None
        with self.__con:
            cur = self.__con.cursor()
            cur.execute(statement)
            data = cur.fetchall()
            cur.close()
        return data

    def execute_statement_many(self, statement, values):
        with self.__con:
            cur = self.__con.cursor()
            cur.executemany(statement, values)
            self.__con.commit()
            cur.close()

    def query_all_tables(self):
        statement = "SHOW tables"
        return self.execute_statement_with_ret(statement)

    def create_table_with_delete(self, table_name, key, columns):
        statement = "DROP TABLE IF EXISTS `%s`" % table_name
        self.execute_statement(statement)
        self.create_table(table_name, key, columns)

    def create_table(self, table_name, key, columns):
        col = ""
        for string in columns:
            col += string + ", "
        statement = "CREATE TABLE IF NOT EXISTS`" + self.__db_name + """`.`%s`(%sPRIMARY KEY(`%s`))""" \
                                                                     % (table_name, col, key)
        self.execute_statement(statement)

    def insert_many(self, table, columns, values):
        col_length = len(columns.split(','))
        columns_num = "%s" + ", %s" * (col_length - 1)
        statement = """INSERT INTO %s(%s) VALUES(%s)""" % (table, columns, columns_num)
        self.execute_statement_many(statement, values)

    def insert(self, table, column, value):
        statement = """INSERT INTO %s(%s) VALUES(%s)""" % (table, column, value)
        self.execute_statement(statement)

    def query(self, table, column, value=None):
        if value is None:
            statement = """SELECT %s FROM %s""" % (column, table)
        else:
            statement = """SELECT * FROM %s.%s WHERE %s = '%s'""" % (self.__db_name, table, column, value)
        return self.execute_statement_with_ret(statement)

    def query_where(self, table, where=None):
        if where is None:
            statement = """SELECT * FROM %s""" % table
        else:
            statement = """SELECT * FROM %s.%s WHERE %s""" % (self.__db_name, table, where)
        return self.execute_statement_with_ret(statement)





