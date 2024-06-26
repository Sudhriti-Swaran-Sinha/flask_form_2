from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
all_books = []


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///<name of database>.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Creating a table

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"<Book {self.title} by {self.author} data: {self.rating}>"

## After creating the columns need to comment out this code / No need to comment out
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # reading the list of all_books and showing the saved book list
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        books = result.scalars().all()

    return render_template("index.html", all_books=books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        book_name = request.form["book_name"]
        book_author = request.form["book_author"]
        rating = request.form["rating"]

        # Creating the data
        with app.app_context():
            new_book = Book(title=book_name, author=book_author, rating=rating)
            db.session.add(new_book)
            db.session.commit()
            d_book = {
                "title": book_name,
                "author": book_author,
                "rating": rating
            }
            all_books.append(d_book)
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit"):
def change_rating():
    render_template("rating.html")
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
