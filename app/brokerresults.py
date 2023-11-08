import mysql.connector
# Set the path to the CA certificate file

MYSQL_HOST = "db-mysql-lon1-10668-do-user-8714569-0.b.db.ondigitalocean.com"
MYSQL_USER = "doadmin"
MYSQL_PASSWORD = "AVNS_yYlaUe6YWhbGhvki97L"
MYSQL_DATABASE = "broker_dump"
MYSQL_DATABASE_LEGACY = "hastec_stacks"

ca_cert_path = 'ca-certificate.crt'
# Connect to the MySQL server


def get_broker_logs():
    connection2 = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=25060,
        ssl_ca=ca_cert_path,

    )

# Do something with the connection
# ...
    cursor2 = connection2.cursor()

    query = (
        "SELECT timestamp as timestamp, "
        "topic as topic, "
        "message as message, "
        "id as id "
        "FROM broker_messages "
        "ORDER BY timestamp DESC"
    )

    cursor2.execute(query)

    row = cursor2.fetchone()

    timestamps = []
    topic = []
    message = []
    id = []
    list_data = []

    while row is not None:
        timestamps.append(row[0])
        topic.append(row[1])
        message.append(row[2])
        id.append(row[3])
        result_json = {"timestamps": row[0],
                       "topic": row[1], "id": row[3], "message": row[2]}
        list_data.append(result_json)
        row = cursor2.fetchone()

    cursor2.close()
    connection2.close()
    return list_data
