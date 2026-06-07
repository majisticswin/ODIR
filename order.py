# order.py
# Favourite Books order placement and invoice generation

from datetime import datetime


class OrderItem:
    """A line item copied from the selected book when the order is placed."""

    def __init__(self, book, quantity):
        self.book = book
        self.quantity = quantity
        self.unit_price = book.price

    def line_total(self):
        return round(self.quantity * self.unit_price, 2)


class Order:
    """A confirmed customer order with the books and agreed prices stored."""

    def __init__(self, order_id, customer_name, delivery_address, items):
        self.order_id = order_id
        self.customer_name = customer_name
        self.delivery_address = delivery_address
        self.items = items
        self.order_date = datetime.now()
        self.status = "Confirmed"

    def total_price(self):
        return round(sum(item.line_total() for item in self.items), 2)


class Invoice:
    """The billing document created once the order has been confirmed."""

    def __init__(self, invoice_id, order):
        self.invoice_id = invoice_id
        self.order = order
        self.issue_date = datetime.now()
        self.payment_message = "Payment has been processed."

    def total_payable(self):
        return self.order.total_price()

    def to_dict(self):
        return {
            "invoice_id": self.invoice_id,
            "order_id": self.order.order_id,
            "customer_name": self.order.customer_name,
            "delivery_address": self.order.delivery_address,
            "issue_date": self.issue_date.strftime("%d/%m/%Y %H:%M"),
            "status": self.order.status,
            "payment_message": self.payment_message,
            "order_items": [
                {
                    "book_id": item.book.book_id,
                    "title": item.book.title,
                    "author": item.book.author,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "line_total": item.line_total(),
                }
                for item in self.order.items
            ],
            "total_payable": self.total_payable(),
        }


class OrderManager:
    """Controller that places the order and creates the invoice."""

    def __init__(self, catalogue_manager):
        self.catalogue_manager = catalogue_manager
        self.orders = {}
        self.invoices = {}
        self.next_order_number = 1
        self.next_invoice_number = 1

    def place_order(self, customer_name, delivery_address, book_id, quantity):
        return self.place_order_from_items(
            customer_name=customer_name,
            delivery_address=delivery_address,
            checkout_items=[{"book_id": book_id, "quantity": quantity}]
        )

    def place_order_from_items(self, customer_name, delivery_address, checkout_items):
        # This is used for both the cart checkout and direct book order
        customer_name = customer_name.strip()
        delivery_address = delivery_address.strip()

        # Basic validation is done before any stock is changed
        if not customer_name:
            raise ValueError("Customer name cannot be blank")
        if not delivery_address:
            raise ValueError("Delivery address cannot be blank")
        if not checkout_items:
            raise ValueError("Order must contain at least one item")

        order_items = []
        for checkout_item in checkout_items:
            # Each checkout item is checked before it becomes an order item
            book_id = self._read_checkout_value(checkout_item, "book_id")
            quantity = int(self._read_checkout_value(checkout_item, "quantity"))

            if quantity < 1:
                raise ValueError("Quantity must be at least 1")

            book = self.catalogue_manager.get_book_by_id(book_id)
            if not book:
                raise ValueError("Selected book was not found")
            if book.stock < quantity:
                raise ValueError("Not enough stock is available for this book")

            order_items.append(OrderItem(book, quantity))

        order = Order(self._next_order_id(), customer_name, delivery_address, order_items)
        invoice = Invoice(self._next_invoice_id(), order)

        # Stock is only reduced after the full order has passed validation
        for item in order_items:
            item.book.stock -= item.quantity

        self.orders[order.order_id] = order
        self.invoices[invoice.invoice_id] = invoice
        return order, invoice

    def _read_checkout_value(self, checkout_item, field_name):
        # Allows checkout data to come from either the cart or a direct order
        if isinstance(checkout_item, dict):
            return checkout_item.get(field_name)
        return getattr(checkout_item, field_name)

    def get_invoice(self, invoice_id):
        return self.invoices.get(invoice_id)

    def _next_order_id(self):
        order_id = f"ORD{self.next_order_number:03d}"
        self.next_order_number += 1
        return order_id

    def _next_invoice_id(self):
        invoice_id = f"INV{self.next_invoice_number:03d}"
        self.next_invoice_number += 1
        return invoice_id
