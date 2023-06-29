import pyodbc
import dbConnect


def list_all_procedures(connectionPacket: dbConnect.connectionPacket):
    sql = """select
	            ROUTINE_SCHEMA,
	            ROUTINE_NAME
            from INFORMATION_SCHEMA.ROUTINES
            where ROUTINE_TYPE = 'PROCEDURE';"""
    connectionPacket.cursor.execute(sql)
    row = connectionPacket.cursor.fetchone()
    while row:
        print(row)
        row = connectionPacket.cursor.fetchone()
        
def run_procedure(connectionPacket: dbConnect.connectionPacket, procedure: str, input: list):
    sql = "EXECUTE " + procedure
    if (input is not None):
        sql = sql + " "
        for _ in range(len(input) - 1):
            sql = sql + "?, "
        sql = sql + "?"
        try:
            connectionPacket.cursor.execute(sql, tuple(input))
        except pyodbc.Error as ex:
            print(ex.args[1])
            
def print_query_result(connectionPacket: dbConnect.connectionPacket):
    row = connectionPacket.cursor.fetchone()
    while row:
        print(row)
        row = connectionPacket.cursor.fetchone()