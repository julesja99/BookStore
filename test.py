import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",                     # hostname
    user = "root",                          # the user who has privlege to the db
    passwd = "9114",        # passwd for user
    auth_plugin = 'mysql_native_password',
    database = "testdb"                     #name my own
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE testdb")

# mycursor.execute("CREATE TABLE Author (name VARCHAR(20), age smallint UNSIGNED, authorID int PRIMARY KEY AUTO_INCREMENT")

# mycursor.execute("DESCRIBE Author") # how table looks like 

# mycursor.execute("INSERT INTO Author (name, age) VALUES (%s, %s)", ("Author Z", 55)) # don't have to put author ID since auto-incremented
# mydb.commit()

# mycursor.execute("SELECT * FROM Author")
#for x in mycursor:
    #print(x)



