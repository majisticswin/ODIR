# catalogue.py

class Catalogue:
    """Stores all books and categories."""

    def __init__(self):
        self.books = {}        # book_id - Book
        self.categories = {}   # category_id - BookCategory

    def add_category(self, category):
        self.categories[category.category_id] = category

    def add_book(self, book):
        self.books[book.book_id] = book

    def get_all_books(self):
        return list(self.books.values())

    def get_all_categories(self):
        return list(self.categories.values())

    def get_book_by_id(self, book_id):
        return self.books.get(book_id)

    def search(self, query):
        """Search by title, author, or ISBN (case-insensitive)."""
        q = query.lower()
        return [
            b for b in self.books.values()
            if q in b.title.lower() or q in b.author.lower() or q in b.isbn
        ]

    def filter_by_category(self, category_id):
        return [b for b in self.books.values() if b.category.category_id == category_id]


class CatalogueManager:
    """Controller for all catalogue operations."""

    def __init__(self, catalogue):
        self.catalogue = catalogue

    def get_all_books(self):
        return self.catalogue.get_all_books()

    def get_all_categories(self):
        return self.catalogue.get_all_categories()

    def get_book_by_id(self, book_id):
        return self.catalogue.get_book_by_id(book_id)

    def search_books(self, query):
        if not query.strip():
            return self.catalogue.get_all_books()
        return self.catalogue.search(query)

    def filter_by_category(self, category_id):
        return self.catalogue.filter_by_category(category_id)

    def is_in_stock(self, book_id):
        book = self.catalogue.get_book_by_id(book_id)
        return book.is_in_stock() if book else False