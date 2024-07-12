from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import sqlalchemy as sa
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask import Flask, render_template, request
import smtplib


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
def get_all_posts():
    user = Book(title="Harry Potter", author="J. K. Rowling", review=9.3)
    db.session.add(user)
    db.session.commit()

    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars()

    with app.app_context():
        book = db.session.execute(
            db.select(Book).where(Book.title == "Harry Potter")).scalar()

    with app.app_context():
        book_to_update = db.session.execute(
            db.select(Book).where(Book.title == "Harry Potter")).scalar()
        book_to_update.title = "Harry Potter and the Chamber of Secrets"
        db.session.commit()

    book_id = 1
    with app.app_context():
        book_to_update = db.session.execute(
            db.select(Book).where(Book.id == book_id)).scalar()
        # or book_to_update = db.get_or_404(Book, book_id)
        book_to_update.title = "Harry Potter and the Goblet of Fire"
        db.session.commit()

    with app.app_context():
        book_to_delete = db.session.execute(
            db.select(Book).where(Book.id == book_id)).scalar()
        # or book_to_delete = db.get_or_404(Book, book_id)
        db.session.delete(book_to_delete)
        db.session.commit()

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
