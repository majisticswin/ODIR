# Order and Invoice Integration Notes

This branch adds the order placement and invoice generation part.

## Main file

`order.py` contains:

- `OrderManager`
- `Order`
- `OrderItem`
- `Invoice`

This is the main part that should be used after checkout is confirmed.

## Method for checkout to call

For a cart with one or more items, call:

```python
order, invoice = order_manager.place_order_from_items(
    customer_name=customer_name,
    delivery_address=delivery_address,
    checkout_items=[
        {"book_id": "B009", "quantity": 1},
        {"book_id": "B011", "quantity": 2},
    ]
)
```

`checkout_items` can be a list of dictionaries with `book_id` and `quantity` values. The method validates the details, checks stock, creates the order, reduces stock and creates the invoice.

There is also a smaller helper for a single book test:

```python
order, invoice = order_manager.place_order(customer_name, delivery_address, book_id, quantity)
```

## Temporary test page

The route below is only for testing this part before the full cart and checkout page is connected:

`/order/<book_id>`

The template below is also only a test page:

`templates/order_form.html`

Another page can call `OrderManager` instead of using this test page.

## Invoice page

`templates/invoice.html` displays the generated invoice. It shows the order and invoice details, selected books, quantities, agreed unit prices and total payable.

The invoice does not show the remaining stock level. Stock is checked and updated internally by `OrderManager`, while customer-facing pages only show availability.

## Tests

Run:

```bash
python -m unittest tests.test_order -v
```
