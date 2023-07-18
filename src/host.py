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
    new_dbPacket = dbConnect.connect(dbConfig)
    if new_dbPacket.isValid is False:
        exit(-1)
    request = "idle"
    while request != "quit":
        request = input("""
                        'quit' to quit\n
                        'list procedures' to see all available procedures\n
                        'list tables' to see all tables\n
                        'run procedure' to select and run a procedure\n""")
        match request:
            case "quit":
                new_dbPacket.close()
                exit(0)
            case "list procedures":
                new_dbPacket.list_all_procedures()
            case "list tables":
                new_dbPacket.list_all_tables()
            case "run procedure":
                procedure = input("input procedure name: ")
                value = input("input parameters, separate by space: ")
                new_dbPacket.run_procedure(procedure, value)
                
                visualize = input("print result? Y/N")
                if (visualize == "Y"):
                    new_dbPacket.print_query_result()
            case "columns":
                print(new_dbPacket.run_query_wResult(sql="select * from dbo.component"))
                #for column in new_dbPacket.cursor.columns(table='component'):
                    #print(column.column_name)
            
        new_dbPacket.connection.commit()

