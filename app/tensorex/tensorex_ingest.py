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


# Close the cursor and connection
schedule.every(1).seconds.do(get_queries)

while True:
    schedule.run_pending()
    time.sleep(0.1)
