import pyodbc
import uuid
import datetime

def invoke_sql_insert(request_id, request_date, request_targ, request_expr, request_requ):
    
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    try:
        cnxn.autocommit = False
        result = cursor.execute(
                    "INSERT INTO MichaelScott (RequestID, RequestDateTime, RequestTarget, RequestExpression, RequestRequester) VALUES (?, ?, ?, ?, ?)", 
                    request_id, request_date, request_targ, request_expr, request_requ
                )        
        #row = cursor.fetchone()
        #while row:
        #    print (str(row[0]) + " " + str(row[1]))
        #    row = cursor.fetchone()
    except pyodbc.DatabaseError as err:
        print(err)
        cnxn.rollback()
        cnxn.close()
        return err
    else:
        cnxn.commit()
    finally:
        cnxn.autocommit = True
    
    cnxn.close()
    return result.rowcount

def invoke_sql_query(request_id):
    
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    
    result = cursor.execute(
                "SELECT RequestResult FROM MichaelScott WHERE RequestID = ?", 
                request_id
            )

    row = cursor.fetchone()
    cnxn.close()
    return row

def request_ps_expression(request_targ, request_expr, request_requ):
    request_id = str(uuid.uuid4())
    request_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row_count = invoke_sql_insert(request_id, request_date, request_targ, request_expr, request_requ)
    if row_count:
        result = invoke_sql_query(request_id)[0]
        while result == None:
            result = invoke_sql_query(request_id)[0]

    return result


server = ''
database = 'Bots'
username = ''
password = ''
driver= '{ODBC Driver 17 for SQL Server}'

#request_id = str(uuid.uuid4())
#request_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#request_targ = "ASL-DHCP04" 
#request_expr = "Get-Process"
#request_requ = "rafael.gustmann@uniasselvi.com.br"

#print(request_ps_expression(request_targ, request_expr, request_requ))

#invoke_sql_insert(request_id, request_date, request_targ, request_expr, request_requ)
#invoke_sql_query("85c17672-b20c-4ee4-b6d7-76c613ac0535")