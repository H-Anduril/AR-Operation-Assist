import pyodbc
import dbConnect
import query


if __name__ == '__main__':
    
    print("Connection Started\n")
    dbConfig = dbConnect.dbConfig(
        'S011DDB0003',
        'AR_GOA_POC',
        'AR_User',
        'T@@sM22n'
    )
    new_connectionPacket = dbConnect.connect(dbConfig)
    if new_connectionPacket.isValid is False:
        exit(-1)
    request = "idle"
    while request != 'q':
        request = input("press q to quit; press 't' to test input; press 's' to test view\n")
        if (request == 't'):
            procedure = "create_component"
            values = [-4, 'TEST', 'TEST_VENDOR', 'TEST_IMAGE', '/user/documents']
            query.run_procedure(new_connectionPacket, procedure, values)
            
        elif request == 's':
            query.list_all_procedures(new_connectionPacket)
            query.print_query_result(new_connectionPacket);
        new_connectionPacket.connection.commit()
    
    new_connectionPacket.close()
    exit(0)
        
