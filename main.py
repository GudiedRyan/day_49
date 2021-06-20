from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Library %r>' % self.name


all_books = []


@app.route('/')
def home():
    books = db.session.query(Library).all()
    return render_template("index.html", books=books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        rating = float(request.form['rating'])
        book = Library(name=name, author=author, rating=rating)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    book = Library.query.get_or_404(id)
    if request.method == 'POST':
        book.rating = float(request.form['rating'])
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book = book)

@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    book = Library.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))
        


if __name__ == "__main__":
    app.run(debug=True)

