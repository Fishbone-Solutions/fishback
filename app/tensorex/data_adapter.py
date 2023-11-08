import mysql.connector
import typing
# Set the path to the CA certificate file

MYSQL_HOST = "db-mysql-lon1-10668-do-user-8714569-0.b.db.ondigitalocean.com"
MYSQL_USER = "doadmin"
MYSQL_PASSWORD = "AVNS_yYlaUe6YWhbGhvki97L"
MYSQL_DATABASE = "tensorex_demo"
ca_cert_path = 'ca-certificate.crt'


def get_stack_height(device_id, db_table, start_time, end_time):
    connection_ = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database='tensorex_demo',
        port=25060,
        ssl_ca=ca_cert_path,)

# Do something with the connection
# ...
    DBcursor = connection_.cursor()

    query = "SELECT FROM_UNIXTIME(timestamp) AS timestamp"\
            "stack_height, ambient_temp " \
            "FROM stack_height " \
            "WHERE timestamp >= UNIX_TIMESTAMP(NOW() - INTERVAL 20 MINUTE)" \
            "ORDER BY timestamp DESC"

    DBcursor.execute(query)

    row = DBcursor.fetchone()

    timestamps = []
    stack_heights = []
    temperatures = []

    while row is not None:
        now = row[0]
        timestamp_ = int(now.timestamp()) - 3600
        timestamps.append(timestamp_)
        stack_heights.append(row[1])
        temperatures.append(row[2])
        row = DBcursor.fetchone()

    response_json = {
        "timestamps": timestamps,
        "dataseries": [{
            "name": "Stack Heights",
            "data": stack_heights,
        },
            {
            "name": "Ambient Temperature",
            "data": temperatures,
        },

        ]
    }
# Close the cursor and connection
    DBcursor.close()
    connection_.close()

    return response_json
