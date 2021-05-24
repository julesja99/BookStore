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

#populate super manager (the first manager in this database)
sql_super = "INSERT INTO User VALUES ('super', 'pbkdf2:sha256:150000$p7JqM0su$0b955952898483884cd3e884e5e7fddcf0da71d23b5c95b1de7663bce7bedb05', 1, 'super manager', '11111111', 'city', 0)"

#insert into book--done
sql_book = "INSERT INTO Book (bookID, title, isbn13, language_code, num_pages, publication_date, publisher, cost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
val_book = [
  (1,'Harry Potter and the Half-Blood Prince', '9780439785969', 'eng', 652, '2006-09-16','Scholastic Inc.', 18.99),
  (2,'Harry Potter and the Order of the Phoenix', '9780439358071', 'eng', 870, '2004-09-01','Scholastic Inc.', 17.99),
  (3,'Harry Potter and the Chamber of Secrets (Harry Potter  #2)', '9780439554893', 'eng', 352, '2003-11-01','Scholastic Inc.', 19.00),
  (4,'A Short History of Nearly Everything', '9780767908184', 'eng', 544, '2004-09-14','Broadway Books', 24.00),
  (5,'J.R.R. Tolkien 4-Book Boxed Set: The Hobbit and The Lord of the Rings', '9780345538376', 'eng', 1728, '2012-09-25','Ballantine Books', 12.25),
  (6,'Hatchet', '9780689840920', 'eng', 208, '2000-04-01','Richard Jackson Books', 20.90),
  (7,'The Lord of the Rings (The Lord of the Rings  #1-3)', '9780618517657', 'eng', 1184, '2004-10-21','Houghton Mifflin Harcourt', 15.00),
  (8,'Uncommon Carriers', '9780374280390', 'en-US', 248, '2006-05-16','Farrar Straus Giroux', 8.90),
  (9,'Tropic of Capricorn', '9780802151827', 'eng', 348, '1994-01-13','Grove Press',13.10),
  (10,'Treasure Island', '9781402714573', 'en-US', 213, '2004-10-01','Sterling Children\'s Books', 7.89),
  (11,'Treasure Island', '9780517221143', 'en-US', 272, '2002-09-03','Gramercy Books', 10.90)
]

# insert into Author -- done
sql_author = "INSERT INTO Author (authorID, authorName) VALUES (%s, %s)"
val_author = [
  (1,'J.K. Rowling'),
  (2,'Mary GrandPré'),
  (3,'Bill Bryson'),
  (4,'J.R.R. Tolkien'),
  (5,'Gary Paulsen'),
  (6,'John McPhee'),
  (7,'Henry Miller'),
  (8,'Robert Louis Stevenson'),
  (9,'Scott McKowen'),
  (10,'Milo Winter')
]

# insert into Writes
sql_writes = "INSERT INTO Writes (authorID, bookID) VALUES (%s, %s)"
val_writes = [
    (1, 1), 
    (1, 2),
    (1, 3),
    (2, 1),
    (2, 2),
    (3, 4),
    (4, 5),
    (5, 6),
    (4, 7),
    (6, 8),
    (7, 9),
    (8, 10),
    (8, 11),
    (9, 10),
    (10, 11)
]

sql_comment = ('INSERT INTO Comment (commenter, book_score, text_review, bookID) VALUES (%s, %s, %s, %s)')
val_comment = [
  ('julie',3,'',1), 
  ('julie',4,'',2),
  ('julie',3,'',3), 
  ('julie',4,'',4),
  ('julie',3,'',5), 
  ('julie',4,'',6),
  ('julie',3,'',7), 
  ('julie',4,'',8),
  ('julie',4,'',9),
  ('julie',3,'',10), 
  ('julie',4,'',11)
]
# mycursor.executemany(sql_book, val_book)
# mycursor.executemany(sql_author, val_author)
# mycursor.executemany(sql_writes, val_writes)
# mycursor.execute(sql_super)
#mycursor.executemany(sql_comment, val_comment)

#mydb.commit()

mycursor.execute("SELECT * FROM author")
for x in mycursor:
  print(x)