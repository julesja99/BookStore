import mysql.connector
class db_operations:
    def __init__(self, db_name):
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="9114", 
        auth_plugin="mysql_native_password",
        database=db_name
)
        
    def searchBooks(self, title, author, degree_authorship, publisher, language_code, order_by):
        mycursor = self.mydb.cursor()
        
        books = []

        if title != '': # if user input title
            if order_by == 'year':
                mycursor.execute('SELECT isbn13, title, publication_date, average_rating FROM (SELECT isbn13, title, publication_date, bookID FROM Book WHERE title LIKE %s) B INNER JOIN (select bookID, AVG(book_score) average_rating from Comment GROUP BY bookID) C ON C.bookID = B.bookID ORDER BY publication_date', ('%' + title + '%',)) 

            elif order_by == 'average_rating':
                mycursor.execute('SELECT isbn13, title, publication_date, average_rating FROM (SELECT isbn13, title, publication_date, bookID FROM Book WHERE title LIKE %s) B INNER JOIN (select bookID, AVG(book_score) average_rating from Comment GROUP BY bookID) C ON C.bookID = B.bookID ORDER BY average_rating', ('%' + title + '%',)) 

            else:
                mycursor.execute('SELECT isbn13, title, publication_date, average_rating FROM (SELECT isbn13, title, publication_date, bookID FROM Book WHERE title LIKE %s) B INNER JOIN (select bookID, AVG(book_score) average_rating from Comment GROUP BY bookID) C ON C.bookID = B.bookID ORDER BY publication_date, average_rating', ('%' + title + '%',)) 

            
            for data in mycursor.fetchall():
                book = dict()
                book['isbn13'] = data[0]
                book['title'] = data[1]
                book['publication_date'] = data[2]
                book['average_rating'] = data[3]
                books.append(book)

        if author != '':
            if degree_authorship == 1:
                if order_by == 'year':
                    mycursor.execute('select isbn13, title, publication_date, average_rating FROM Book B INNER JOIN (select bookID from (select * from Writes GROUP BY bookID HAVING COUNT(authorID) = 1) W INNER JOIN (select authorID from author where authorName = %s) A ON W.authorID = A.authorID) R ON B.bookID = R.bookID order by publication_date', (author,))
                elif order_by == 'average_rating':
                    mycursor.execute('select isbn13, title, publication_date, average_rating FROM Book B INNER JOIN (select bookID from (select * from Writes GROUP BY bookID HAVING COUNT(authorID) = 1) W INNER JOIN (select authorID from author where authorName = %s) A ON W.authorID = A.authorID) R ON B.bookID = R.bookID order by average_rating', (author,))
                else:
                    mycursor.execute('select isbn13, title, publication_date, average_rating FROM Book B INNER JOIN (select bookID from (select * from Writes GROUP BY bookID HAVING COUNT(authorID) = 1) W INNER JOIN (select authorID from author where authorName = %s) A ON W.authorID = A.authorID) R ON B.bookID = R.bookID order by publication_date, average_rating', (author,))
                for data in mycursor.fetchall():
                    book = dict()
                    book['isbn13'] = data[0]
                    book['title'] = data[1]
                    book['publication_date'] = data[2]
                    book['average_rating'] = data[3]
                    books.append(book)
            elif degree_authorship == 2:
                if order_by == 'year':
                    mycursor.execute('select isbn13, title, publication_date, average_rating FROM Book B INNER JOIN (select bookID from (select * from Writes GROUP BY bookID HAVING COUNT(authorID) = 2) W INNER JOIN (select authorID from author where authorName = %s) A ON W.authorID = A.authorID) R ON B.bookID = R.bookID order by publication_date', (author,))
                elif order_by == 'average_rating':
                    mycursor.execute('select isbn13, title, publication_date, average_rating FROM Book B INNER JOIN (select bookID from (select * from Writes GROUP BY bookID HAVING COUNT(authorID) = 2) W INNER JOIN (select authorID from author where authorName = %s) A ON W.authorID = A.authorID) R ON B.bookID = R.bookID order by average_rating', (author,))
                else:
                    mycursor.execute('select isbn13, title, publication_date, average_rating FROM Book B INNER JOIN (select bookID from (select * from Writes GROUP BY bookID HAVING COUNT(authorID) = 2) W INNER JOIN (select authorID from author where authorName = %s) A ON W.authorID = A.authorID) R ON B.bookID = R.bookID order by publication_date, average_rating', (author,))
                for data in mycursor.fetchall():
                    book = dict()
                    book['isbn13'] = data[0]
                    book['title'] = data[1]
                    book['publication_date'] = data[2]
                    book['average_rating'] = data[3]
                    books.append(book)

        if publisher != '':
            if order_by == 'year':
                mycursor.execute('SELECT isbn13, title, publication_date, average_rating FROM (SELECT * FROM Book WHERE publisher = %s) B INNER JOIN (select bookID, AVG(book_score) average_rating from Comment GROUP BY bookID) C ON C.bookID = B.bookID ORDER BY publication_date', (publisher,))
            elif order_by == 'average_rating':
                mycursor.execute('SELECT isbn13, title, publication_date, average_rating FROM (SELECT * FROM Book WHERE publisher = %s) B INNER JOIN (select bookID, AVG(book_score) average_rating from Comment GROUP BY bookID) C ON C.bookID = B.bookID ORDER BY average_rating', (publisher,))
            
                
            else: 
                mycursor.execute('SELECT isbn13, title, publication_date, average_rating FROM (SELECT * FROM Book WHERE publisher = %s) B INNER JOIN (select bookID, AVG(book_score) average_rating from Comment GROUP BY bookID) C ON C.bookID = B.bookID ORDER BY publication_date, average_rating', (publisher,))
            
            for data in mycursor.fetchall():
                book = dict()
                book['isbn13'] = data[0]
                book['title'] = data[1]
                book['publication_date'] = data[2]
                book['average_rating'] = data[3]
                books.append(book)

        if language_code != '':

            if order_by == 'year':
                mycursor.execute('SELECT isbn13, title, publication_date, average_rating FROM (SELECT * FROM Book WHERE language_code = %s) B INNER JOIN (select bookID, AVG(book_score) average_rating from Comment GROUP BY bookID) C ON C.bookID = B.bookID ORDER BY publication_date', (language_code,))
            
            elif order_by == 'average_rating':
                mycursor.execute('SELECT isbn13, title, publication_date, average_rating FROM (SELECT * FROM Book WHERE language_code = %s) B INNER JOIN (select bookID, AVG(book_score) average_rating from Comment GROUP BY bookID) C ON C.bookID = B.bookID ORDER BY average_rating', (language_code,))
            
            else: 
                mycursor.execute('SELECT isbn13, title, publication_date, average_rating FROM (SELECT * FROM Book WHERE language_code = %s) B INNER JOIN (select bookID, AVG(book_score) average_rating from Comment GROUP BY bookID) C ON C.bookID = B.bookID ORDER BY publication_date, average_rating', (language_code,))
            
            
            for data in mycursor.fetchall():
                book = dict()
                book['isbn13'] = data[0]
                book['title'] = data[1]
                book['publication_date'] = data[2]
                book['average_rating'] = data[3]
                books.append(book)
    

        return books #return this back to main.py
