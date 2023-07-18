import pyodbc

class dbPacket:
    def __init__(self, isValid, cursor, connection):
        self.isValid = isValid
        self.cursor = cursor
        self.connection = connection
    
    def close(self):
        self.cursor.close()
        self.connection.close()
        self.isValid = False
        
    def list_all_procedures(self):
        sql = """select
	                ROUTINE_SCHEMA,
	                ROUTINE_NAME
                from INFORMATION_SCHEMA.ROUTINES
                where ROUTINE_TYPE = 'PROCEDURE';"""
        self.cursor.execute(sql)
        self.print_query_result()
    
    def list_all_tables(self):
        sql = r"select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_NAME not like '%sys%'"
        self.cursor.execute(sql)
        self.print_query_result()
            
    def run_procedure(self, procedure: str, input: str):
        sql = "DECLARE @return_value int;\nEXECUTE @return_value = " + procedure
        if (len(input) > 0):
            input = list(input.split(" "))
            print(input)
            sql = sql + " "
            for _ in range(len(input) - 1):
                sql = sql + "?, "
            sql = sql + "?;\n"
            sql = sql + "SELECT 'Return Value' = @return_value;"
            print(sql)
            try:
                self.cursor.execute(sql, tuple(input))
            except pyodbc.Error as ex:
                print(ex.args[1])
        else:
            try:
                sql = sql + ";\n" "SELECT 'Return Value' = @return_value;"
                self.cursor.execute(sql)
            except pyodbc.Error as ex:
                print(ex.args[1])    
                
    def print_query_result(self):
        row = self.cursor.fetchone()
        while row:
            print(row)
            row = self.cursor.fetchone()
        while self.cursor.nextset():
            row = self.cursor.fetchone()
            while row:
                print(row)
                row = self.cursor.fetchone()
                
    def write_query_result(self) -> list:
        buf = []
        row = self.cursor.fetchone()
        while row:
            buf.append(row)
            row = self.cursor.fetchone()
        while self.cursor.nextset():
            row = self.cursor.fetchone()
            while row:
                buf.append(row)
                row = self.cursor.fetchone()
        return buf
            
    def run_query(self, sql: str, input=""):
        if len(input) > 0:
            self.cursor.execute(sql, tuple(list(input.split(" "))))
        else:
            self.cursor.execute(sql)
        self.print_query_result()
    
    def run_query_wResult(self, sql: str, input="") -> list:
        if len(input) > 0:
            self.cursor.execute(sql, tuple(list(input.split(" "))))
        else:
            self.cursor.execute(sql)
        return self.write_query_result()
    

class dbConfig():
    def __init__(self, server, database, username, password):
        dbConfig.server = server
        dbConfig.database = database
        dbConfig.username = username
        dbConfig.password = password

# RETURN cursor if connection is successful; 
def connect(dbConfig):
    new_dbPacket = dbPacket(False, None, None)
    driver_name = ''
    driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
    if len(driver_names) > 0:
        driver_name = '{' + driver_names[0] + '}'
    if driver_name:
        connect_str = 'DRIVER={};SERVER={};DATABASE={};ENCRYPT=no;UID={};PWD={}'.format(
            driver_name,
            dbConfig.server,
            dbConfig.database,
            dbConfig.username,
            dbConfig.password
        )
    else:
        print("No suitable driver found. Connection Failed")
        return new_dbPacket
    # print(connect_str)
    
    try:
        cnxn = pyodbc.connect(connect_str)
        print("Connection is working")
        new_dbPacket.isValid = True
        new_dbPacket.cursor = cnxn.cursor()
        new_dbPacket.connection = cnxn
    except pyodbc.Error as ex:
        print(ex.args[1])
        print("Connection Failed")
    return new_dbPacket
