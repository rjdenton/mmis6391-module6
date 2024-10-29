from flask import render_template, request, redirect, url_for
from . import app
from .db_connect import get_db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT book.name, author.name 
        FROM book 
        JOIN author 
        ON book.author_id = author.author_id
    """)
    books = cursor.fetchall()
    return render_template('books.html', books=books)


@app.route('/authors')
def authors():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM author")
    authors = cursor.fetchall()
    return render_template('authors.html', authors=authors)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        cursor = db.cursor()
        cursor.execute("INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)",
                       (name, email, message))
        db.commit()
        cursor.close()

        return redirect(url_for('contact'))

    return render_template('contact.html')