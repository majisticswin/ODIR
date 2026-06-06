import unittest

from book import Book, BookCategory
from catalogue import Catalogue, CatalogueManager
from order import OrderManager


class OrderPlacementAndInvoiceTests(unittest.TestCase):
    def setUp(self):
        self.category = BookCategory("CAT005", "Technology")
        self.catalogue = Catalogue()
        self.catalogue.add_category(self.category)
        self.book = Book(
            "B009",
            "978-0-201-63361-0",
            "Design Patterns",
            "Gang of Four",
            59.99,
            4,
            self.category,
            "23 foundational design patterns for object-oriented software."
        )
        self.catalogue.add_book(self.book)
        self.catalogue_manager = CatalogueManager(self.catalogue)
        self.order_manager = OrderManager(self.catalogue_manager)

    def test_order_is_created_with_invoice_from_book_and_quantity(self):
        order, invoice = self.order_manager.place_order(
            customer_name="John Smith",
            delivery_address="123 Name Street, City State 0000",
            book_id="B009",
            quantity=2
        )

        self.assertEqual(order.customer_name, "John Smith")
        self.assertEqual(order.delivery_address, "123 Name Street, City State 0000")
        self.assertEqual(order.status, "Confirmed")
        self.assertEqual(order.items[0].book.book_id, "B009")
        self.assertEqual(order.items[0].quantity, 2)
        self.assertEqual(order.total_price(), 119.98)
        self.assertEqual(invoice.order.order_id, order.order_id)
        self.assertEqual(invoice.total_payable(), 119.98)
        self.assertEqual(self.book.stock, 2)

    def test_blank_customer_name_is_not_accepted(self):
        with self.assertRaises(ValueError) as error:
            self.order_manager.place_order("", "123 Name Street", "B009", 1)

        self.assertIn("Customer name cannot be blank", str(error.exception))

    def test_quantity_must_be_one_or_more(self):
        with self.assertRaises(ValueError) as error:
            self.order_manager.place_order("John Smith", "123 Name Street", "B009", 0)

        self.assertIn("Quantity must be at least 1", str(error.exception))

    def test_out_of_stock_order_is_not_accepted(self):
        with self.assertRaises(ValueError) as error:
            self.order_manager.place_order("John Smith", "123 Name Street", "B009", 6)

        self.assertIn("Not enough stock", str(error.exception))

    def test_order_can_be_created_from_checkout_items(self):
        second_book = Book(
            "B011",
            "978-1-56619-909-4",
            "Refactoring",
            "Martin Fowler",
            54.50,
            3,
            self.category,
            "Improving the design of existing code."
        )
        self.catalogue.add_book(second_book)

        order, invoice = self.order_manager.place_order_from_items(
            customer_name="John Smith",
            delivery_address="123 Name Street, City State 0000",
            checkout_items=[
                {"book_id": "B009", "quantity": 1},
                {"book_id": "B011", "quantity": 2},
            ]
        )

        self.assertEqual(len(order.items), 2)
        self.assertEqual(order.items[0].book.book_id, "B009")
        self.assertEqual(order.items[1].book.book_id, "B011")
        self.assertEqual(order.total_price(), 168.99)
        self.assertEqual(invoice.total_payable(), 168.99)
        self.assertEqual(self.book.stock, 3)
        self.assertEqual(second_book.stock, 1)


if __name__ == "__main__":
    unittest.main()
