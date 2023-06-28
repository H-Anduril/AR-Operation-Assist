import pyodbc

class cursorPacket:
    def __init__(self, isValid, cursor, connection):
        self.isValid = isValid
        self.cursor = cursor
        self.connection = connection
    
    def close(self):
        self.cursor.close()
        self.connection.close()
        self.isValid = False

class dbConfig():
    def __init__(self, server, database, username, password):
        dbConfig.server = server
        dbConfig.database = database
        dbConfig.username = username
        dbConfig.password = password

# RETURN cursor if connection is successful; 
def connect(dbConfig):
    new_cursorPacket = cursorPacket(False, None, None)
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
        return new_cursorPacket
    print(connect_str)
    
    try:
        cnxn = pyodbc.connect(connect_str)
        print("Connection is working")
        new_cursorPacket.isValid = True
        new_cursorPacket.cursor = cnxn.cursor()
        new_cursorPacket.connection = cnxn
    except pyodbc.Error as ex:
        # print(ex.args[1])
        print("Connection Failed")
    return new_cursorPacket
