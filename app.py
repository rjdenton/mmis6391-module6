from flask import Flask, render_template, request, redirect, url_for
import MySQLdb

app = Flask(__name__)

# MySQL connection (update with your details)
db = MySQLdb.connect(
    host="h40lg7qyub2umdvb.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    user="mj5b848egset7xai",
    passwd="d8lt7o6neb61isxu",
    db="ooh6ad18uxd9wkjd"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
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
    cursor = db.cursor()
    cursor.execute("SELECT name FROM author")
    authors = cursor.fetchall()
    return render_template('authors.html', authors=authors)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
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

if __name__ == '__main__':
    app.run(debug=True)


