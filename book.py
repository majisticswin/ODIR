# book.py

class BookCategory:
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name


class Book:
    def __init__(self, book_id, isbn, title, author, price, stock, category, description=""):
        self.book_id = book_id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock
        self.category = category
        self.description = description

    def is_in_stock(self):
        return self.stock > 0

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "price": self.price,
            "stock": self.stock,
            "in_stock": self.is_in_stock(),
            "category_id": self.category.category_id,
            "category_name": self.category.name,
            "description": self.description,
        }