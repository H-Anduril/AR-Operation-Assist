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
        request = input("press q to quit\n")
    
    new_cursorPacket.close()
    exit(0)
        
