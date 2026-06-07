"""Data class for a single shopping cart item."""

import time


class CartItem:
    """A data holder representing a single item in the shopping cart."""

    def __init__(self, book_id, title, price, quantity, added_at=None):
        self.book_id = book_id
        self.title = title
        self.price = price
        self.quantity = quantity
        self.added_at = added_at or time.time()

    def is_expired(self, timeout_seconds=86400):
        # Checks whether the cart item has been left for too long
        return (time.time() - self.added_at) > timeout_seconds

    def to_dict(self):
        # Converts the cart item into data that can be saved or displayed
        return {
            "book_id": self.book_id,
            "title": self.title,
            "price": self.price,
            "quantity": self.quantity,
            "added_at": self.added_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            book_id=data["book_id"],
            title=data["title"],
            price=data["price"],
            quantity=data["quantity"],
            added_at=data.get("added_at"),
        )
