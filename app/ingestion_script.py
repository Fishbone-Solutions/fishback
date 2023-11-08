import mysql.connector
from mysql.connector import Error
import json
import schedule
import time
import ast
import uuid

MYSQL_HOST = "db-mysql-lon1-10668-do-user-8714569-0.b.db.ondigitalocean.com"
MYSQL_USER = "doadmin"
MYSQL_PASSWORD = "AVNS_yYlaUe6YWhbGhvki97L"
MYSQL_DATABASE = "tensorex_demo"
MYSQL_DATABASE_LEGACY = "broker_dump"
CA_CERT_PATH = 'ca-certificate.crt'
def get_data():
    # establish connection to MySQL server
    try:
        connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE_LEGACY,
        port=25060,
        ssl_ca=CA_CERT_PATH,

    )
        device_connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=25060,
        ssl_ca=CA_CERT_PATH,

    )

        # create a cursor object to execute SQL queries
        cursor = connection.cursor()
        device_cursor = device_connection.cursor()

        # execute a SELECT query to fetch all rows from the broker_messages table
        query = "SELECT * FROM broker_messages"
        cursor.execute(query)
        row = cursor.fetchone()
        while row is not None:
            if row[1] == 'tensorx_frag1':
                current_row = row[2]
                payload = ast.literal_eval(current_row)
                if isinstance(payload,bytes) == 1:
                    print(payload,type(payload))
                    string = payload.decode('utf-8')
                    lst = ast.literal_eval(string)
                    timestamp = lst[0]['TS']
                    check_query = "SELECT * FROM stack_height WHERE timestamp = %s"
                    check_values = [(payload[0]['TS'])]
                    secondary_payload = ast.literal_eval(payload[0]['VR'])
                    stack_raw = secondary_payload[1]
                    stack_raw = stack_raw * 0.022
                    stack_height = round(stack_raw,2)
                    temperature = int(secondary_payload[7])
                    temperature = int(temperature/400)
                    ambient_temperature = round(temperature, 2)
                    print(timestamp,stack_raw,temperature)
                    device_cursor.execute(check_query, check_values)
                    result = device_cursor.fetchall()
                    for row in result:
                          try:
                            insert_query = ("INSERT INTO tensorex_devices "
                    "(stack_height, device_datapoint, device_id, timestamp, ambient_temperature) "
                    "VALUES (%s, %s, %s, %s, %s)")
                            values = (stack_height, datapoint_id, stack_id, timestamp, ambient_temperature)
                            cursor.execute(insert_query, values)
                            connection.commit()
                          except Exception as e:
                            print(f"An error occurred: {e}")
                


                #dct = ast.literal_eval(payload)
                
                
                
                       
                
       

    except Error as e:
        print(f"Error connecting to MySQL server: {e}")

   

# call the get_data() function and print the fetched rows

schedule.every(2).seconds.do(get_data)

while True:
    schedule.run_pending()
    time.sleep(0.1)
