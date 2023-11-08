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
    print("Script Intial")
    connection2 = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE_LEGACY,
        port=25060,
        ssl_ca=CA_CERT_PATH,

    )
    connection1_ins = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=25060,
        ssl_ca=CA_CERT_PATH,

    )
    cursor2 = connection2.cursor()

    query = (
        "SELECT timestamp as timestamp, topic as topic, message as message from broker_messages")

    cursor2.execute(query)
    row = cursor2.fetchone()
    print(row)
    while row is not None:
        # insert stack height,timestamp
        if row[1] == 'tensorx_frag1':
            payload = json.loads((row[2]))
            print(payload)
            if len(payload[0]['VR']) == 8:
                timestamps = payload[0]['TS']
                stack_raw = payload[0]['VR'][1]
                temperature = payload[0]['VR'][6]
                temperature = temperature/400
                temperature_ = round(temperature, 2)
                mycursor = connection1_ins.cursor()
                check_query = "SELECT * FROM stack_height WHERE timestamp = %s"
                check_values = [(payload[0]['TS'])]
                mycursor.execute(check_query, check_values)
                result = mycursor.fetchone()
                if not result:
                    try:
                        insert_query = "INSERT INTO stack_height (timestamp, stack_height,ambient_temp) VALUES (%s, %s,%s)"
                        values = [
                            (timestamps, "{:.2f}".format(stack_raw * 0.022), temperature_)]
                        mycursor.executemany(insert_query, values)
                        connection1_ins.commit()
                    except Exception as e:
                        print(f"An error occurred: {e}")
                row = cursor2.fetchone()
                cursor2.close()
                connection2.close()


# Close the cursor and connection

schedule.every(1).seconds.do(get_queries)

while True:
    schedule.run_pending()
    time.sleep(0.1)
