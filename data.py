# seed_data.py

from book import Book, BookCategory


def seed_catalogue(catalogue):
    """Load sample categories and books into the catalogue."""

    fiction    = BookCategory("CAT001", "Fiction")
    science    = BookCategory("CAT002", "Science")
    history    = BookCategory("CAT003", "History")
    children   = BookCategory("CAT004", "Children")
    technology = BookCategory("CAT005", "Technology")

    for cat in [fiction, science, history, children, technology]:
        catalogue.add_category(cat)

    books = [
        Book("B001", "978-0-7432-7356-5", "The Great Gatsby",        "F. Scott Fitzgerald",  14.99,  13, fiction,    "A portrait of the Jazz Age and Jay Gatsby's obsession with Daisy Buchanan."),
        Book("B002", "978-0-06-112008-4", "To Kill a Mockingbird",   "Harper Lee",           15.99,   82, fiction,    "A story of racial injustice seen through the eyes of young Scout Finch."),
        Book("B003", "978-0-14-028329-7", "1984",                    "George Orwell",        13.99,  22, fiction,    "A dystopian novel following Winston Smith under a totalitarian regime."),
        Book("B004", "978-0-14-028381-5", "Sapiens",                 "Yuval Noah Harari",    22.99,  15, history,    "A brief history of humankind from the Stone Age to the present."),
        Book("B005", "978-0-385-33348-1", "A Brief History of Time", "Stephen Hawking",      19.99,   5, science,    "Hawking explains the universe from the Big Bang to black holes."),
        Book("B006", "978-0-385-49081-6", "Guns, Germs, and Steel",  "Jared Diamond",        21.99,   9, history,    "Why some civilisations came to dominate others across history."),
        Book("B007", "978-0-590-35340-3", "Harry Potter and the Philosopher's Stone", "J. K. Rowling", 16.99, 55, children, "Harry discovers he is a wizard and begins his journey at Hogwarts."),
        Book("B008", "978-0-7356-6745-7", "Clean Code",              "Robert C. Martin",     49.99,  10, technology, "A guide to writing clean, readable, and maintainable code."),
        Book("B009", "978-0-201-63361-0", "Design Patterns",         "Gang of Four",         59.99,   40, technology, "23 foundational design patterns for object-oriented software."),
        Book("B010", "978-0-14-028329-0", "Pride and Prejudice",     "Jane Austen",          11.99,   0, fiction,    "The story of Elizabeth Bennet and Mr Darcy. (Out of stock)"),
    ]

    for book in books:
        catalogue.add_book(book)