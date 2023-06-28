import pyodbc
import dbConnect


if __name__ == '__main__':
    
    print("Connection Started\n")
    dbConfig = dbConnect.dbConfig(
        'S011DDB0003',
        'AR_GOA_POC',
        'AR_User',
        'T@@sM22n'
    )
    new_cursorPacket = dbConnect.connect(dbConfig)
    if new_cursorPacket.isValid is False:
        exit(-1)
    request = "idle"
    while request != 'q':
        request = input("press q to quit; press 't' to test input; press 's' to test view\n")
        if (request == 't'):
            sql = """EXECUTE dbo.create_component ?, ?, ?, ?, ?"""
            values = (-2, 'TEST', 'TEST_VENDOR', 'TEST_IMAGE', '/user/documents')
            new_cursorPacket.cursor.execute(sql, values)
            
        elif request == 's':
            new_cursorPacket.cursor.execute("SELECT * FROM dbo.component")
            row = new_cursorPacket.cursor.fetchone()
            while row:
                print(row)
                row = new_cursorPacket.cursor.fetchone()
    
        new_cursorPacket.connection.commit()
    
    new_cursorPacket.close()
    exit(0)
        
