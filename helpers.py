import pyodbc
import uuid
import datetime
import json

def invoke_sql_insert(request_id, request_date, request_targ, request_expr, request_reqi, request_reqn):
    
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    try:
        cnxn.autocommit = False
        result = cursor.execute(
                    "INSERT INTO MichaelScott (RequestID, RequestDateTime, RequestTarget, RequestExpression, RequestRequesterAadObjectId, RequestRequesterName) VALUES (?, ?, ?, ?, ?, ?)", 
                    request_id, request_date, request_targ, request_expr, request_reqi, request_reqn
                )        
        #row = cursor.fetchone()
        #while row:
        #    print (str(row[0]) + " " + str(row[1]))
        #    row = cursor.fetchone()
    except pyodbc.DatabaseError as err:
        print(err)
        cnxn.rollback()        
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

def request_ps_expression(request_targ, request_expr, request_reqi, request_reqn):
    request_id = str(uuid.uuid4())
    request_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row_count = invoke_sql_insert(request_id, request_date, request_targ, request_expr, request_reqi, request_reqn)
    if row_count:
        result = invoke_sql_query(request_id)
        while result[0] == None:
            result = invoke_sql_query(request_id)

    return json.loads(result[0])


server = 'sqlserver.grupouniasselvi.local'
database = 'Bots'
username = 'bots-michaelscott'
password = 'Xunda33..'
driver= '{ODBC Driver 17 for SQL Server}'

#request_id = str(uuid.uuid4())
#request_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#request_targ = "ASL-DHCP04" 
#request_expr = "Get-Process"
#request_requ = "rafael.gustmann@uniasselvi.com.br"

#print(request_ps_expression(request_targ, request_expr, request_requ))

#invoke_sql_insert(request_id, request_date, request_targ, request_expr, request_requ)
#invoke_sql_query("85c17672-b20c-4ee4-b6d7-76c613ac0535")