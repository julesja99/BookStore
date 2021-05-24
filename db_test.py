import mysql.connector
from werkzeug.security import generate_password_hash

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9114", 
    auth_plugin="mysql_native_password",
    database="test"
)

class db_operations:
    def __init__(self, db_name):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="9114", 
            auth_plugin="mysql_native_password",
            database=db_name
        )
    
    def register(self, cursor, username, password, fullname, phone_num, address):
        result_list = []
        sql = "INSERT INTO User (loginName, password, role, name, phoneNumber, address) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (username, password, 0, fullname, phone_num, address)
        cursor.execute(sql, val)
        mydb.commit()
        for data in cursor:
            result_list.append(list(data))
        return result_list
