# app.py
# Favourite Books — Area 2: Browse Catalogue & Search Books

from flask import Flask, render_template, request, jsonify
from catalogue import Catalogue, CatalogueManager
from data import seed_catalogue

app = Flask(__name__)

# Bootstrap: creates catalogue, loads data, wraps in manager
catalogue = Catalogue()
seed_catalogue(catalogue)
manager = CatalogueManager(catalogue)


@app.route("/")
def index():
    categories = manager.get_all_categories()
    return render_template("index.html", categories=categories)


@app.route("/search")
def search():
    query    = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    if query:
        books = manager.search_books(query)
    else:
        books = manager.get_all_books()

    if category:
        books = [b for b in books if b.category.category_id == category]

    return jsonify([b.to_dict() for b in books])


@app.route("/book/<book_id>")
def book_detail(book_id):
    book = manager.get_book_by_id(book_id)
    if not book:
        return "Book not found", 404
    return render_template("book_detail.html", book=book.to_dict())


if __name__ == "__main__":
    app.run(debug=True)