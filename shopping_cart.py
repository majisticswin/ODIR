"""Shopping cart management for the Favourite Books app."""

from cart_item import CartItem

CART_COLOURS = [
    "#2d2b6b", "#4a1a6b", "#1a3a5c",
    "#3b2800", "#1a3b1a", "#1a1a3b",
]


class ShoppingCart:
    """Manages a customer's shopping cart before checkout."""

    def __init__(self, customer_id, catalogue_manager):
        self.customer_id = customer_id
        self.catalogue_manager = catalogue_manager
        self.items = []

    def add_item(self, book_id, quantity=1):
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")

        book = self.catalogue_manager.get_book_by_id(book_id)
        if book is None:
            raise ValueError(f"Book '{book_id}' not found in catalogue.")
        if not book.is_in_stock():
            raise ValueError(f"'{book.title}' is out of stock.")

        existing = self._find_item(book_id)
        # If the book is already in the cart, its quantity is increased instead
        new_quantity = quantity if existing is None else existing.quantity + quantity
        if book.stock < new_quantity:
            raise ValueError("Not enough stock is available for this book.")

        if existing:
            existing.quantity = new_quantity
        else:
            self.items.append(CartItem(
                book_id=book.book_id,
                title=book.title,
                price=book.price,
                quantity=quantity,
            ))

    def remove_item(self, book_id):
        item = self._find_item(book_id)
        if item is None:
            raise ValueError(f"Item '{book_id}' not found in cart.")
        self.items.remove(item)

    def update_quantity(self, book_id, quantity):
        # Updates the cart amount but still checks the available stock
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")

        item = self._find_item(book_id)
        if item is None:
            raise ValueError(f"Item '{book_id}' not found in cart.")

        book = self.catalogue_manager.get_book_by_id(book_id)
        if book is None:
            raise ValueError(f"Book '{book_id}' not found in catalogue.")
        if book.stock < quantity:
            raise ValueError("Not enough stock is available for this book.")

        item.quantity = quantity

    def remove_expired_items(self):
        self.items = [item for item in self.items if not item.is_expired()]

    def calculate_total(self):
        return round(sum(item.price * item.quantity for item in self.items), 2)

    def get_display_items(self):
        display_items = []
        for index, item in enumerate(self.items):
            entry = item.to_dict()
            book = self.catalogue_manager.get_book_by_id(item.book_id)
            entry["colour"] = CART_COLOURS[index % len(CART_COLOURS)]
            entry["line_total"] = round(item.price * item.quantity, 2)
            entry["author"] = book.author if book else ""
            entry["category"] = book.category.name if book else "Book"
            display_items.append(entry)
        return display_items

    def checkout_items(self):
        # Sends only the details needed by the order manager at checkout
        return [
            {"book_id": item.book_id, "quantity": item.quantity}
            for item in self.items
        ]

    def clear_cart(self):
        self.items = []

    def _find_item(self, book_id):
        for item in self.items:
            if item.book_id == book_id:
                return item
        return None
