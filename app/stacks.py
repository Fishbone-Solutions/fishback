import time
import mysql.connector
MYSQL_HOST = "db-mysql-lon1-10668-do-user-8714569-0.b.db.ondigitalocean.com"
MYSQL_USER = "doadmin"
MYSQL_PASSWORD = "AVNS_yYlaUe6YWhbGhvki97L"
MYSQL_DATABASE = "hastec_stacks"
ca_cert_path = 'ca-certificate.crt'
# Connect to the MySQL server


def save_stack_data(response):
    data = response
    data.update({'request_id': str(time.time())})

    try:
        # Connect to the database
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=25060,
            ssl_ca=ca_cert_path,
        )

        cursor = cnx.cursor()

        # Insert the data into the table
        insert_query = f"INSERT INTO  stack_register({', '.join(data.keys())}) VALUES ({', '.join(['%s']*len(data))})"
        values = tuple(data.values())
        cursor.execute(insert_query, values)
        cnx.commit()

    except Exception as e:
        # Handle the exception
        print(f"An error occurred: {e}")
        return 'Error'

    finally:
        # Close the database connection
        cursor.close()
        cnx.close()

    return 'Success'
