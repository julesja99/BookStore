'''
export FLASK_APP=main.py
$ export FLASK_ENV=development
$ flask run
'''
import mysql.connector
import db_test
from flask import Flask, redirect, render_template, request, flash, session, g
from flask.helpers import url_for
from werkzeug.security import generate_password_hash, check_password_hash


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9114", 
    auth_plugin="mysql_native_password",
    database="test"
)
app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods = ('POST', 'GET'))
def register():
    mycursor = mydb.cursor()

    if request.method == 'POST':
        
        username = request.form['loginName']
        password = request.form['password']
        name = request.form['name']
        phone_number = request.form['phoneNumber']
        address = request.form['address']

        error = None

        mycursor.execute('SELECT name FROM user WHERE loginName = %s', (username,))
        
        if mycursor.fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
            
        if error is None:
            sql = "INSERT INTO User (loginName, password, role, name, phoneNumber, address) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (username, generate_password_hash(password), 0, name, phone_number, address)
            mycursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for('register_success', loginName = username))
            
        flash(error)
    return render_template('register.html')


@app.route('/register_manager', methods = ('POST', 'GET'))
def register_manager():
    mycursor = mydb.cursor()

    if request.method == 'POST':
        
        username = request.form['loginName']
        password = request.form['password']
        name = request.form['name']
        phone_number = request.form['phoneNumber']
        address = request.form['address']

        error = None

        mycursor.execute('SELECT name FROM user WHERE loginName = %s', (username,))
        if mycursor.fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
            
        if error is None:
            sql = "INSERT INTO User (loginName, password, role, name, phoneNumber, address) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (username, generate_password_hash(password), 1, name, phone_number, address)
            mycursor.execute(sql, val)
            mydb.commit()
            redirect(url_for('register_success', loginName = username))
        flash(error)
    return render_template('register_manager.html')

@app.route('/register_success/<loginName>')
def register_success(loginName):

    return render_template('register_success.html', loginName = loginName) 

@app.route('/login', methods=('GET', 'POST'))
def login():
    mycursor = mydb.cursor()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        error = None
        
        mycursor.execute('SELECT * FROM user WHERE loginName = %s', (username,))
        user = mycursor.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[1], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            session['role'] = user[2]
            return redirect('/searchbook')

        flash(error)

    return render_template('login.html')

@app.before_request
def load_logged_in_user():
    mycursor = mydb.cursor()
    loginName = session.get('user_id')

    if loginName is None:
        g.user = None
    else:
        mycursor.execute('SELECT * FROM User WHERE loginName = %s', (loginName,))
        g.user = mycursor.fetchone()
        
@app.route('/book/<isbn>', methods=('GET', 'POST'))
def book(isbn):
    mycursor = mydb.cursor()
    book = dict()
    comments = []

    book_sql = mycursor.execute('SELECT * FROM Book WHERE isbn13 = %s', (isbn,))
    sql_result = book_sql.fetchone()

    book['isbn13'] = sql_result[2] # 9780439358071
    book['title'] = sql_result[1]
    book['language_code'] = sql_result[3]
    book['num_pages'] = sql_result[4]
    book['publication_date'] = sql_result[5]
    book['publisher'] = sql_result[6]
    book['cost'] = sql_result[7]
    book['stock_level'] = sql_result[8]
    bookID_for_comment = sql_result[0]

    # review comments
    mycursor.execute('select isbn13, title, book_score, text_review, usefulness, commenter FROM Comment C LEFT JOIN Book B ON C.bookID = B.bookID where B.isbn13 = %s', (isbn,))
    for data in mycursor.fetchall():
        comment_dict = dict()
        comment_dict['isbn13'] = data[0]
        comment_dict['title'] = data[1]
        comment_dict['book_score'] = data[2]
        comment_dict['text_review'] = data[3]
        comment_dict['usefulness'] = data[4]
        comment_dict['commenter'] = data[5]
        comments.append(comment_dict)

    # write a comment
    if request.method == 'POST':
        submitted = request.form['submit']
        username = session.get('user_id')

        if submitted == "Leave comment":
            book_score = request.form['book_score']
            text_review = request.form['text_review']
            

            # if user already left comment on the same book

            mycursor.execute('select bookID from Book WHERE isbn13 = %s', (isbn,))
            bookID = mycursor.fetchone()[0]

            mycursor.execute('insert into comment (commenter, book_score, text_review, bookID) VALUES (%s, %s, %s, %s)', (username, book_score, text_review, bookID))
            
            mydb.commit()    

        elif submitted == "Rate comment":
            # if user is not himself
            usefulness = request.form['usefulness'] 
            commenter = request.form['commenter'] 
            #update usefulness if rated
            mycursor.execute("UPDATE comment SET usefulness = usefulness+ %s WHERE commenter = %s AND bookID = %s", (usefulness, commenter, bookID_for_comment))
            mydb.commit()
        elif submitted == "Place order":
            # if ordering more than stock_level

            num_copy = request.form['num_copy']

            mycursor.execute('select cost from book where bookID = %s', (bookID_for_comment,))
            amount = mycursor.fetchone()[0] * num_copy

            # update stock level
            mycursor.execute('update book set stock_level = stock_level - %s where bookID = %s', (num_copy, bookID_for_comment))
            mycursor.execute('insert into orders (bookID, loginName, num_copy, amount) VALUES (%s, %s, %s, %s)', (bookID_for_comment, username, num_copy, amount))

            mydb.commit()
    return render_template('book.html', book=book, comments = comments)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

        
@app.route('/searchbook', methods=('GET', 'POST'))
def searchBook():
    
    if request.method == 'POST':
        
        title = request.form['title']
        author = request.form['author']
        degree_authorship = request.form['degree_authorship']
        publisher = request.form['publisher']
        language_code = request.form['language_code']

        order_by = request.form['order_by']

        db_opr_obj = db_test.db_operations("test") # use sql script
        books = db_opr_obj.searchBook(title, author, degree_authorship, publisher,language_code, order_by)



        
    return render_template('browse_book.html', books = books)


@app.route('/browse_profile', methods=('GET', 'POST'))
def browse_profile():
    mycursor = mydb.cursor()
    target_dict = dict()
    comments =[]
    if request.method == 'POST':
        username = request.form['username']
    # fetch basic information
        mycursor.execute('SELECT loginName, name, address, num_trusters FROM User WHERE role = 0 AND loginName = %s', (username,))
        target = mycursor.fetchone()
        target_dict['name']= target[1]
        target_dict['address']= target[2]
        target_dict['num_trusters']= target[3]


        # get the target's comments
        mycursor.execute('select isbn13, title, book_score, text_review, usefulness FROM Comment C LEFT JOIN Book B ON C.bookID = B.bookID where commenter = %s', (username,))

        for data in mycursor.fetchall():
            comment_dict = dict()
            comment_dict['isbn13'] = data[0]
            comment_dict['title'] = data[1]
            comment_dict['book_score'] = data[2]
            comment_dict['text_review'] = data[3]
            comment_dict['usefulness'] = data[4]
            comments.append(comment_dict)

    return render_template('browse_profile.html', target = target_dict, comments = comments)


@app.route('/order', methods=('GET', 'POST'))
def order():
    mycursor = mydb.cursor()

    
@app.route('/recommend')
def recommend():
    mycursor = mydb.cursor()
    books = []
    mycursor.execute('select bookID from Order where loginName = (select loginName from Order where loginName != %s AND bookID = (select bookID from Order where loginName = %s))', ('julie','julie',))
    for data in mycursor.fetchall():
        book_dict = dict()
        book_dict['bookID'] = data[0]
        books.append(book_dict)
    render_template('recommend.html', books = books)



# manager dashboard
@app.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    mycursor = mydb.cursor()
    books = []
    authors = []
    publishers= []
    trusted_users = []
    useful_users = []
    if request.method == 'POST':
        submitted = request.form['submit']
        if submitted == "View books":

            num_book = request.form['num_book']
            
            #list of m popular books (in terms of copies sold)
            book_sql = mycursor.execute('select bookID, sum(amount) from Orders GROUP BY bookID ORDER BY sum(amount) DESC limit %s', (num_book,))
            
            for data in book_sql.fetchall():
                book_dict = dict()
                book_dict['bookID'] = data[0]
                book_dict['sum_amount'] = data[1]
                books.append(book_dict)

        #list of m popular authors (in terms of copies sold)
        elif submitted == "View authors":
            num_authors = request.form['num_authors']
            auth_sql = mycursor.execute('select authorID, sum_amount from Writes W inner join (select bookID, sum(amount) as sum_amount from orders GROUP BY bookID) O on W.bookID = O.bookID ORDER BY sum_amount DESC limit %s', (num_authors,))
            for data in auth_sql.fetchall():
                auth_dict = dict()
                auth_dict['authorID'] = data[0]
                auth_dict['sum_amount'] = data[1]
                authors.append(auth_dict)

        #list of m popular publisher (in terms of copies sold)
        elif submitted == "View publishers":
            num_publishers = request.form['num_publishers']
            
            #list of m popular books (in terms of copies sold)
            pub_sql = mycursor.execute('select publisher, sum_amount from Book B inner join (select bookID, sum(amount) AS sum_amount from Orders GROUP BY bookID) O ON B.bookID = O.bookID ORDER BY sum_amount DESC limit %s', (num_publishers,))

            
            for data in book_sql.fetchall():
                pub_dict = dict()
                pub_dict['publisher'] = data[0]
                pub_dict['sum_amount'] = data[1]
                publishers.append(pub_dict)
        # top n most trusted users (number of trusters)
        # top n most useful users (usefulness combined)


    return render_template('dashboard.html', books = books, authors = authors, publishers = publishers)

@app.route('/stock', methods=('GET', 'POST'))
def manage_stock():
    mycursor = mydb.cursor()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn13 = request.form['isbn13']
        language_code = request.form['language_code']
        num_pages = request.form['num_pages']
        publication_date = request.form['publication_date']
        publisher = request.form['publisher']
        cost = request.form['cost']
        stock_level = request.form['stock_level']

    
        mycursor.execute('SELECT bookID FROM Book WHERE isbn13 = %s', (isbn13,))
        if mycursor.fetchone() is not None:
            mycursor.execute('UPDATE book SET stock_level = %s WHERE isbn13 = %s', (stock_level, isbn13))
            mydb.commit()
        elif mycursor.fetchone() is None:
            mycursor.execute('INSERT INTO Book (title, isbn13, language_code, num_pages, publication_date, publisher, cost, stock_level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (title, isbn13, language_code, num_pages, publication_date, publisher, cost, stock_level))
            mydb.commit()
    return render_template('stock_management.html')

if __name__ == '__main__':
   app.run(debug = True)