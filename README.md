# 🏪 Favourite Books — Online Bookstore

> **CS30003 — Assignment 3: Design Implementation**  
A lightweight online bookstore built with **Python (Flask)** and **HTML/CSS**, split across four feature areas developed independently by each team member.

---

## Team & Module Ownership

| Area | Feature | Developer |
|------|---------|-----------|
| **1** | Customer Account (Register / Login / Logout) | Mitul Joarder |
| **2** | Browse Book Catalogue & Search | Dan Thammisetty |
| **3** | Manage Shopping Cart | Mun Yong Deng |
| **4** | Place Order & Invoice | Alexander Ozimkovsky-Klein |

Each developer works in their own section. Where integration into shared files (`App.py`, `index.html`) was needed, additions are marked with comments and no existing code was touched.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Flask |
| Templating | Jinja2 (via Flask) |
| Frontend | HTML5, CSS3 (no frameworks) |
| Fonts | Google Fonts (Inter, Merriweather) |
| Data store | JSON flat file (`customers.json`) |
| Password hashing | `hashlib` SHA-256 (Python stdlib) |
| Session management | Flask server-side sessions |

---

## Project Structure

```
ODIR/
├── static/
│   └── cart.css                  # Stylesheet for cart and invoice pages
│
├── templates/
│   ├── account.html              # Account dashboard
│   ├── book_detail.html          # Individual book page
│   ├── cart.html                 # Shopping cart
│   ├── index.html                # Catalogue landing page
│   ├── invoice.html              # Order confirmation / invoice
│   ├── login.html                # Sign-in form
│   ├── order_form.html           # Single-book order form
│   └── register.html             # Registration form
│
├── tests/
│   ├── test_cart_order_flow.py
│   └── test_order.py
│
├── App.py                        # Main Flask app — all routes
├── book.py                       # Book and BookCategory models
├── cart_item.py                  # CartItem model
├── catalogue.py                  # Catalogue and CatalogueManager
├── customer.py                   # Customer model + JSON persistence
├── customers.json                # Flat-file customer database
├── data.py                       # Seed data (10 books, 5 categories)
├── order.py                      # Order, OrderItem, Invoice, OrderManager
├── shopping_cart.py              # ShoppingCart logic
├── README.md
└── LICENSE
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Setup

```bash
# 1. Enter the project directory
cd ODIR

# 2. Install dependencies
pip install flask

# 3. Run the app
python App.py
```

The server starts at **http://127.0.0.1:5000**

---

## URL Routes

| Method | URL | Description | Area |
|--------|-----|-------------|------|
| `GET` | `/` | Catalogue landing page | 2 |
| `GET` | `/search` | Search / filter books (returns JSON) | 2 |
| `GET` | `/book/<book_id>` | Individual book detail page | 2 |
| `GET` | `/cart` | View shopping cart | 3 |
| `POST` | `/cart/add` | Add item to cart | 3 |
| `POST` | `/cart/remove` | Remove item from cart | 3 |
| `POST` | `/cart/update` | Update item quantity | 3 |
| `POST` | `/cart/checkout` | Place order from cart | 3 & 4 |
| `GET/POST` | `/order/<book_id>` | Single-book order form | 4 |
| `GET` | `/register` | Registration form | 1 |
| `POST` | `/register` | Submit new account | 1 |
| `GET` | `/login` | Login form | 1 |
| `POST` | `/login` | Authenticate user | 1 |
| `GET` | `/logout` | Sign out, redirect to home | 1 |
| `GET` | `/account` | Account dashboard (requires login) | 1 |

---

## Module Details

### Area 1 — Customer Account
**Developer:** Mitul Joarder  
**Files:** `customer.py`, `register.html`, `login.html`, `account.html`

- Registration with server-side validation (required fields, password length, duplicate email check)
- Login with email + password; stores first name in Flask session
- Account dashboard, login-protected via session check
- Logout clears session and redirects home
- Form values preserved on validation failure so users don't retype everything
- Nav bar dynamically shows Login or the logged-in user's name using `session` in Jinja2

### Area 2 — Browse Book Catalogue
**Developer:** Dan Thammisetty  
**Files:** `book.py`, `catalogue.py`, `data.py`, `index.html`, `book_detail.html`

- Responsive book grid with colour-coded category covers
- Live search by title, author, or ISBN via `fetch()` to `/search`
- Category filter dropdown
- Individual book detail page with ISBN, stock, description, and price
- 10 seed books across 5 categories loaded at startup

### Area 3 — Shopping Cart
**Developer:** Mun Yong Deng  
**Files:** `shopping_cart.py`, `cart_item.py`, `cart.html`

- Add, remove, and update quantities
- Cart items expire after 24 hours
- Stock validation on add and update
- Subtotal calculated from current prices; $4.99 flat shipping when cart is non-empty

### Area 4 — Place Order & Invoice
**Developer:** Alexander Ozimkovsky-Klein  
**Files:** `order.py`, `invoice.html`, `order_form.html`

- Validates customer name, address, and stock availability before confirming
- Stock decremented only after the full order passes validation
- Generates a printable invoice with line totals and order metadata
- Supports both single-book orders and multi-item cart checkout

---

## Data Storage

**Books** are loaded from `data.py` into memory at startup. All catalogue reads run against in-memory Python dicts — no file I/O at runtime.

**Customers** are stored in `customers.json` as a flat JSON array:

```json
[
  {
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "phone": "0412345678",
    "password_hash": "<sha256-hex>"
  }
]
```

The `Customer` class wraps all I/O in `find_by_email()`, `email_exists()`, and `save()` — swapping to a real database later only means rewriting those three methods.

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| CSS per template (no shared stylesheet) | No build tools needed; each page is self-contained |
| SHA-256 for password hashing | In Python stdlib — no extra dependencies |
| Flask server-side sessions | Simple and sufficient for assignment scope |
| JSON flat file for customers | Zero setup; easy to inspect during development |
| Plain HTML forms for auth | More reliable than fetch-based forms; no CORS issues |
| `session` used directly in Jinja2 | Flask injects it automatically; no need to pass it through every route |
| Teammate code never modified | All cross-area additions are marked with comments; only new lines inserted |
