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

#create tables and schema
#mycursor.execute("CREATE TABLE Customer (loginName VARCHAR(30) PRIMARY KEY NOT NULL, password VARCHAR(50) NOT NULL, name VARCHAR(60) NOT NULL, phoneNumber CHAR(11) NOT NULL, address varchar(100) NOT NULL)")
#mycursor.execute("CREATE TABLE Manager (CHECK (loginName <> registrant), loginName VARCHAR(30) PRIMARY KEY NOT NULL, password VARCHAR (50) NOT NULL, name VARCHAR(60) NOT NULL, phoneNumber CHAR(11) NOT NULL, address VARCHAR(100), registrant VARCHAR(30) NOT NULL, CONSTRAINT FK_registrant_tb_Manager FOREIGN KEY (registrant) REFERENCES Manager(loginName))")
#mycursor.execute("CREATE TABLE Book (bookID INT AUTO_INCREMENT PRIMARY KEY, title TEXT, average_rating DECIMAL (3,2) UNSIGNED, isbn VARCHAR(10), isbn13 CHAR(13) NOT NULL, language_code VARCHAR(5), num_pages INT UNSIGNED, ratings_count INT UNSIGNED DEFAULT 0, text_reviews_count INT UNSIGNED DEFAULT 0, publication_date DATE, publisher VARCHAR(50), cost DECIMAL(10, 2) NOT NULL, CHECK (text_reviews_count <= ratings_count))")
#mycursor.execute("CREATE TABLE Comment (commentID INT AUTO_INCREMENT PRIMARY KEY, commenter VARCHAR(30) NOT NULL, book_score DECIMAL (2,1) NOT NULL, text_review TEXT, bookID INT NOT NULL, CONSTRAINT FK_commenter_tb_Comment FOREIGN KEY (commenter) REFERENCES Customer(loginName) ON DELETE CASCADE, CONSTRAINT FK_bookID_tb_Comment FOREIGN KEY (bookID) REFERENCES Book(bookID) ON DELETE CASCADE)")
#mycursor.execute("CREATE TABLE Trust (loginName VARCHAR(30) NOT NULL, truster VARCHAR(30) NOT NULL, CONSTRAINT FK_loginName_tb_Trust FOREIGN KEY (loginName) REFERENCES Customer (loginName) ON DELETE CASCADE, CONSTRAINT FK_truster_tb_Trust FOREIGN KEY (truster) REFERENCES Customer (loginName) ON DELETE CASCADE, CONSTRAINT trustee_truster_not_equal CHECK (loginName <> truster))")
#mycursor.execute("CREATE TABLE Stock (bookID INT NOT NULL, quantity INT UNSIGNED DEFAULT 0, CONSTRAINT FK_bookID_tb_Stock FOREIGN KEY (bookID) REFERENCES Book (bookID) ON DELETE CASCADE)")
#mycursor.execute("CREATE TABLE Author (authorID INT AUTO_INCREMENT PRIMARY KEY, authorName VARCHAR(60) NOT NULL)")
#mycursor.execute("CREATE TABLE Writes (bookID INT NOT NULL, authorID INT NOT NULL, CONSTRAINT FK_bookID_tb_Writes FOREIGN KEY (bookID) REFERENCES Book (bookID) ON DELETE CASCADE, CONSTRAINT FK_authorID_tb_Writes FOREIGN KEY (authorID) REFERENCES Author (authorID) ON DELETE CASCADE)")
#mycursor.execute("CREATE TABLE Orders (orderNumber INT AUTO_INCREMENT PRIMARY KEY, bookID INT NOT NULL, loginName VARCHAR(30) NOT NULL, num_copy INT UNSIGNED DEFAULT 1, amount DECIMAL(10,2) NOT NULL, status VARCHAR(40) NOT NULL, shippingAddress VARCHAR(100) NOT NULL, orderDate DATE DEFAULT(SYSDATE()), CONSTRAINT FK_loginName_tb_Orders FOREIGN KEY (loginName) REFERENCES Customer (loginName) ON DELETE CASCADE, CONSTRAINT FK_bookID_tb_Order FOREIGN KEY (bookID) REFERENCES Book (bookID) ON DELETE CASCADE)")
#mycursor.execute("CREATE TABLE Usefulness (commentID INT NOT NULL, usefulness_score INT UNSIGNED, scorer VARCHAR(30), CONSTRAINT FK_commentID_tb_Usefulness FOREIGN KEY (commentID) REFERENCES Comment (commentID), CONSTRAINT FK_scorer_tb_Usefulness FOREIGN KEY (scorer) REFERENCES Customer (loginName) ON DELETE CASCADE)")


#----------changed-----
mycursor.execute("CREATE TABLE User (loginName VARCHAR(30) PRIMARY KEY NOT NULL, password TEXT NOT NULL, role INT NOT NULL, name VARCHAR(60) NOT NULL, phoneNumber CHAR(11) NOT NULL, address varchar(100) NOT NULL, num_trusters INT UNSIGNED DEFAULT 0)")
mycursor.execute("CREATE TABLE Book (bookID INT AUTO_INCREMENT PRIMARY KEY, title TEXT, isbn13 CHAR(13) NOT NULL, language_code VARCHAR(5), num_pages INT UNSIGNED, publication_date DATE, publisher VARCHAR(50), cost double NOT NULL, stock_level INT UNSIGNED DEFAULT 100)")
mycursor.execute("CREATE TABLE Author (authorID INT AUTO_INCREMENT PRIMARY KEY, authorName VARCHAR(60) NOT NULL)")
mycursor.execute("CREATE TABLE Writes (bookID INT NOT NULL, authorID INT NOT NULL, CONSTRAINT FK_bookID_tb_Writes FOREIGN KEY (bookID) REFERENCES Book (bookID) ON DELETE CASCADE, CONSTRAINT FK_authorID_tb_Writes FOREIGN KEY (authorID) REFERENCES Author (authorID) ON DELETE CASCADE)")
mycursor.execute("CREATE TABLE Comment (commentID INT AUTO_INCREMENT PRIMARY KEY, commenter VARCHAR(30) NOT NULL, book_score DOUBLE NOT NULL, text_review TEXT, bookID INT NOT NULL, usefulness DOUBLE UNSIGNED DEFAULT 0, CONSTRAINT FK_commenter_tb_Comment FOREIGN KEY (commenter) REFERENCES User (loginName) ON DELETE CASCADE, CONSTRAINT FK_bookID_tb_Comment FOREIGN KEY (bookID) REFERENCES Book(bookID) ON DELETE CASCADE)")

mycursor.execute("CREATE TABLE Orders (orderNumber INT AUTO_INCREMENT PRIMARY KEY, bookID INT NOT NULL, loginName VARCHAR(30) NOT NULL, num_copy INT UNSIGNED DEFAULT 1, amount DOUBLE NOT NULL, CONSTRAINT FK_loginName_tb_Orders FOREIGN KEY (loginName) REFERENCES User (loginName) ON DELETE CASCADE, CONSTRAINT FK_bookID_tb_Order FOREIGN KEY (bookID) REFERENCES Book (bookID) ON DELETE CASCADE)")

#------inspect---------
mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)
