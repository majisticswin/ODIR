import unittest

from App import app, carts, manager


class CartOrderFlowTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        carts.clear()

    def test_book_can_be_added_to_cart_and_displayed(self):
        response = self.client.post("/cart/add", data={"book_id": "B009", "quantity": "2"})

        self.assertEqual(response.status_code, 302)
        cart_page = self.client.get("/cart")
        body = cart_page.get_data(as_text=True)
        self.assertIn("Design Patterns", body)
        self.assertIn("119.98", body)

    def test_checkout_places_order_and_shows_invoice(self):
        book = manager.get_book_by_id("B009")
        original_stock = book.stock
        self.client.post("/cart/add", data={"book_id": "B009", "quantity": "1"})

        response = self.client.post(
            "/cart/checkout",
            data={
                "customer_name": "John Smith",
                "delivery_address": "123 Name Street, City State 0000"
            }
        )

        body = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Invoice", body)
        self.assertIn("Design Patterns", body)
        self.assertEqual(book.stock, original_stock - 1)
        self.assertEqual(len(carts["guest"].items), 0)


if __name__ == "__main__":
    unittest.main()
