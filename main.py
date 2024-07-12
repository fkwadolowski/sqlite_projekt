from flask import Flask, render_template, request, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as sa
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask import Flask, render_template, request
import smtplib
from sqlalchemy import select

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# initialize the app with the extension
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    review: Mapped[float] = mapped_column(nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars(select(Book)).all()
    return render_template("index.html", data=all_books)


@app.route("/add", methods=['post', 'get'])
def add():
    if request.method == "POST":
        new_book = Book(title=request.form['title'],
                        author=request.form['author'],
                        review=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    book_id = request.args.get('id')
    with app.app_context():
        book = db.session.execute(
            db.select(Book).filter(Book.id == book_id)
        ).scalar_one_or_none()

    if request.method == "POST":
        new_review = float(request.form['review'])
        with app.app_context():
            book_to_update = db.session.execute(
                db.select(Book).filter(Book.id == book_id)
            ).scalar_one_or_none()
            if book_to_update:
                book_to_update.review = new_review
                db.session.commit()
                return redirect(url_for('home'))
            else:
                return "Book not found", 404

    return render_template('edit.html', data=book)
@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    with app.app_context():
        book_to_delete = db.session.execute(
            db.select(Book).filter(Book.id == book_id)
        ).scalar_one_or_none()
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
