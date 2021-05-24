"""
goal: create all the tables with all my tables with all the dependencies 
      and referential constraints from Phase 1
"""
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="9114",
  auth_plugin="mysql_native_password",
  database="test"
)
 
mycursor = mydb.cursor()

# create database
#mycursor.execute("CREATE DATABASE test") 

#----------create table schemas-----
# mycursor.execute("CREATE TABLE User (loginName VARCHAR(30) PRIMARY KEY NOT NULL, password TEXT NOT NULL, role INT NOT NULL, name VARCHAR(60) NOT NULL, phoneNumber CHAR(11) NOT NULL, address varchar(100) NOT NULL, num_trusters INT UNSIGNED DEFAULT 0)")
# mycursor.execute("CREATE TABLE Book (bookID INT AUTO_INCREMENT PRIMARY KEY, title TEXT, isbn13 CHAR(13) NOT NULL, language_code VARCHAR(5), num_pages INT UNSIGNED, publication_date DATE, publisher VARCHAR(50), cost double NOT NULL, stock_level INT UNSIGNED DEFAULT 100)")
# mycursor.execute("CREATE TABLE Author (authorID INT AUTO_INCREMENT PRIMARY KEY, authorName VARCHAR(60) NOT NULL)")
# mycursor.execute("CREATE TABLE Writes (bookID INT NOT NULL, authorID INT NOT NULL, CONSTRAINT FK_bookID_tb_Writes FOREIGN KEY (bookID) REFERENCES Book (bookID) ON DELETE CASCADE, CONSTRAINT FK_authorID_tb_Writes FOREIGN KEY (authorID) REFERENCES Author (authorID) ON DELETE CASCADE)")
# mycursor.execute("CREATE TABLE Comment (commentID INT AUTO_INCREMENT PRIMARY KEY, commenter VARCHAR(30) NOT NULL, book_score DOUBLE NOT NULL, text_review TEXT, bookID INT NOT NULL, usefulness DOUBLE UNSIGNED DEFAULT 0, CONSTRAINT FK_commenter_tb_Comment FOREIGN KEY (commenter) REFERENCES User (loginName) ON DELETE CASCADE, CONSTRAINT FK_bookID_tb_Comment FOREIGN KEY (bookID) REFERENCES Book(bookID) ON DELETE CASCADE)")

# mycursor.execute("CREATE TABLE Orders (orderNumber INT AUTO_INCREMENT PRIMARY KEY, bookID INT NOT NULL, loginName VARCHAR(30) NOT NULL, num_copy INT UNSIGNED DEFAULT 1, amount DOUBLE NOT NULL, CONSTRAINT FK_loginName_tb_Orders FOREIGN KEY (loginName) REFERENCES User (loginName) ON DELETE CASCADE, CONSTRAINT FK_bookID_tb_Order FOREIGN KEY (bookID) REFERENCES Book (bookID) ON DELETE CASCADE)")

#------inspect---------
mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)
