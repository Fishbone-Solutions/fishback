import json
import mysql.connector
import schedule
import time
import datetime


MYSQL_HOST = "db-mysql-lon1-10668-do-user-8714569-0.b.db.ondigitalocean.com"
MYSQL_USER = "doadmin"
MYSQL_PASSWORD = "AVNS_yYlaUe6YWhbGhvki97L"
MYSQL_DATABASE = "tensorex_demo"
MYSQL_DATABASE_LEGACY = "broker_dump"

CA_CERT_PATH = 'ca-certificate.crt'
# Connect to the MySQL server


def get_queries():
    broker_connection = mysql.connector.connect(
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
    broker_cursor = broker_connection.cursor()


    query = (
        "SELECT timestamp as timestamp, topic as topic, message as message from "
        "broker_messages")

    broker_cursor.execute(query)
    row = broker_cursor.fetchone()
    while row is not None:
        device_cursor = device_connection.cursor()  

        if row[1] == 'tensorx_frag1':
            payload = json.loads((row[2]))
            print(payload)
            if len(payload[0]['VR']) == 8:
                timestamps = payload[0]['TS']
                stack_raw = payload[0]['VR'][1]
                temperature = payload[0]['VR'][6]
                temperature = temperature/400
                temperature_ = round(temperature, 2)
                check_query = "SELECT * FROM stack_height WHERE timestamp = %s"
                check_values = [(payload[0]['TS'])]
                device_cursor.execute(check_query, check_values)
                result = device_cursor.fetchone()
                if not result:
                    try:
                        insert_query = "INSERT INTO stack_height (timestamp, stack_height,ambient_temp) VALUES (%s, %s,%s)"
                        values = [
                            (timestamps, "{:.2f}".format(stack_raw * 0.022), temperature_)]
                        device_cursor.executemany(insert_query, values)
                        device_connection.commit()
                    except Exception as e:
                        print(f"An error occurred: {e}")
                row = broker_cursor.fetchone()
                
               


        # insert stack latitude,longitude,timestamp
        if row[1] == 'tensorx_frag2':
            print("Nothing")
        '''
            payload = json.loads((row[2]))
            if len(payload[0]['VR']) == 2:
                # print("location ", latitude, longitude, int(time.time()))
                mycursor = connection1_ins.cursor()
                check_query = "SELECT * FROM location_data WHERE timestamp = %s"
                check_values = [(int(time.time()))]
                mycursor.execute(check_query, check_values)
                result = mycursor.fetchone()
                if not result:
                    insert_query = "INSERT INTO location_data (timestamp, lat, longitude) VALUES (%s, %s, %s)"
                    values = [(int(time.time()), payload[0]
                               ['VR'][0], payload[0]['VR'][1])]
                    mycursor.executemany(insert_query, values)
                    connection1_ins.commit()
                row = cursor2.fetchone()
    '''                            
       
    


# insert battery,timestamp


# Close the cursor and connection


schedule.every(2).seconds.do(get_queries)

while True:
    schedule.run_pending()
    time.sleep(0.1)
