# 🏪 The Book Haven — Online Bookstore

> **CS30003 — Assignment 3: Design Implementation**
> Swinburne University of Technology · Semester 1, 2026

A lightweight, multi-module online bookstore built with **Python (Flask)** and **HTML/CSS**. The project is structured as four independently developed feature areas, each owned by a separate team member and integrated into a single Flask application.

---

## Table of Contents

1. [Team & Module Ownership](#team--module-ownership)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Getting Started](#getting-started)
5. [URL Routes Reference](#url-routes-reference)
6. [Module Details](#module-details)
   - [Area 1 — Customer Account](#area-1--customer-account)
   - [Area 2 — Browse Book Catalogue](#area-2--browse-book-catalogue)
   - [Area 3 — Shopping Cart](#area-3--shopping-cart)
   - [Area 4 — Place Order & Invoice](#area-4--place-order--invoice)
7. [Data Storage](#data-storage)
8. [Design Decisions](#design-decisions)

---

## Team & Module Ownership

| Area | Feature | Developer |
|------|---------|-----------|
| **1** | Customer Account (Register / Login / Logout) | Mitul Joarder |
| **2** | Browse Book Catalogue & Search | *(teammate)* |
| **3** | Manage Shopping Cart | *(teammate)* |
| **4** | Place Order & Invoice | *(teammate)* |

> Each developer works in their own section. When integration into shared files (`App.py`, `index.html`) was required, additions are clearly marked with `# Added by Mitul` comments and no existing code was modified.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Flask |
| Templating | Jinja2 (via Flask) |
| Frontend | HTML5, CSS3 (no frameworks) |
| Fonts | Google Fonts — Inter, Merriweather |
| Data store | JSON flat file (`customers.json`) |
| Password hashing | `hashlib` SHA-256 (Python stdlib) |
| Session management | Flask server-side sessions |
| Environment | `.venv` (Python virtual environment) |

---

## Project Structure

```
ODIR/
│
├── App.py                  # Main Flask application — all routes
│
├── book.py                 # Book & BookCategory classes         [Area 2]
├── catalogue.py            # Catalogue & CatalogueManager        [Area 2]
├── data.py                 # Seed data (10 books, 5 categories)  [Area 2]
├── customer.py             # Customer class + JSON persistence   [Area 1 — Mitul]
│
├── customers.json          # Flat-file customer database         [Area 1 — Mitul]
│
├── templates/
│   ├── index.html          # Landing page — book catalogue       [Area 2]
│   ├── book_detail.html    # Individual book detail page         [Area 2]
│   ├── register.html       # Account registration form           [Area 1 — Mitul]
│   ├── login.html          # Sign-in form                        [Area 1 — Mitul]
│   └── account.html        # Account dashboard (logged-in)       [Area 1 — Mitul]
│
├── .venv/                  # Python virtual environment
└── .claude/
    └── launch.json         # Dev server launch config
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### 1. Clone / open the project

```bash
cd "ODIR"
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask
```

### 4. Run the application

```bash
python App.py
```

The server starts at **http://127.0.0.1:5000**

---

## URL Routes Reference

| Method | URL | Description | Area |
|--------|-----|-------------|------|
| `GET` | `/` | Book catalogue landing page | 2 |
| `GET` | `/search` | Search / filter books (JSON API) | 2 |
| `GET` | `/book/<book_id>` | Individual book detail page | 2 |
| `GET` | `/register` | Show registration form | 1 |
| `POST` | `/register` | Submit new account | 1 |
| `GET` | `/login` | Show login form | 1 |
| `POST` | `/login` | Authenticate user | 1 |
| `GET` | `/logout` | Clear session, redirect to home | 1 |
| `GET` | `/account` | Account dashboard (login required) | 1 |

---

## Module Details

### Area 1 — Customer Account

**Files:** `customer.py`, `templates/register.html`, `templates/login.html`, `templates/account.html`
**Developer:** Mitul Joarder

#### Features

- **Registration** — Collects first name, last name, email, phone number, password, and confirm password. Server-side validation covers: all fields required, passwords must match, minimum 6-character password, no duplicate emails.
- **Login** — Email + password authentication with inline error feedback.
- **Session persistence** — After login the user's first name is stored in a Flask server-side session. The catalogue nav bar dynamically shows either a **Login** button or the logged-in user's name.
- **Account dashboard** — Displays name, email, and phone. Accessible only when logged in; unauthenticated visits redirect to `/login`.
- **Logout** — Clears the session and redirects to the catalogue home page.
- **Error handling** — Form values are preserved on validation failure so the user doesn't have to retype everything.

#### Customer class (`customer.py`)

```
Customer
├── Attributes: first_name, last_name, email, phone, password_hash
├── hash_password(plain_text)   → SHA-256 hex digest
├── check_password(plain_text)  → bool
├── to_dict() / from_dict()     → serialisation helpers
├── find_by_email(email)        → Customer | None
├── email_exists(email)         → bool
└── save()                      → insert or update in customers.json
```

#### Nav integration (`index.html`)

A conditional block was added to the existing catalogue header (with comments). It uses Flask's built-in `session` Jinja2 global — no changes to the teammate's route were needed:

```html
{% if session.customer_name %}
  <a href="/account">👤 {{ session.customer_name }}</a>
{% else %}
  <a href="/login">Login</a>
{% endif %}
```

---

### Area 2 — Browse Book Catalogue

**Files:** `book.py`, `catalogue.py`, `data.py`, `templates/index.html`, `templates/book_detail.html`

#### Features

- Displays all 10 books in a responsive grid with colour-coded category covers.
- Live search by title, author, or ISBN via a `fetch()` call to `/search`.
- Category filter dropdown (Fiction, Science, History, Children, Technology).
- Individual book detail page showing ISBN, stock count, description, and price.
- "Add to Cart" button placeholder (implemented in Area 3).

#### Class structure

```
BookCategory          Book
├── category_id       ├── book_id, isbn, title, author
└── name              ├── price, stock, category (→ BookCategory)
                      ├── is_in_stock() → bool
                      └── to_dict()     → dict

Catalogue                         CatalogueManager
├── books: dict[id → Book]        ├── get_all_books()
├── categories: dict[id → Cat]    ├── get_all_categories()
├── add_book() / add_category()   ├── get_book_by_id()
├── search(query)                 ├── search_books(query)
└── filter_by_category()          └── is_in_stock(book_id)
```

---

### Area 3 — Shopping Cart

> *(To be implemented by teammate)*

Placeholder "Add to Cart" button exists on `/book/<book_id>`. The cart module will integrate here.

---

### Area 4 — Place Order & Invoice

> *(To be implemented by teammate)*

Will consume session data (customer email) and cart contents from Area 3 to generate an order and printable invoice.

---

## Data Storage

### Books (in-memory)

Books and categories are loaded from `data.py` into memory at startup via `seed_catalogue()`. No file I/O occurs for reads — all catalogue queries run against in-memory Python dictionaries.

### Customers (JSON flat file)

Customer accounts are persisted to `customers.json` in the project root. The format is a JSON array of objects:

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

This flat-file approach was chosen for simplicity during development. The `Customer` class abstracts all I/O behind `find_by_email()`, `email_exists()`, and `save()` — swapping to SQLite or PostgreSQL later only requires rewriting those three methods.

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| All CSS inline per template | Keeps each page self-contained; no build tooling needed |
| SHA-256 password hashing | Available in Python stdlib (`hashlib`); no external dependency |
| Flask `session` for auth state | Simple server-side sessions; no JWT complexity for an assignment scope |
| JSON flat file for customers | Zero setup — works out of the box, easy to inspect during development |
| No JavaScript for auth forms | Plain HTML `<form method="POST">` — simpler, more robust, no fetch/CORS issues |
| `session` used directly in Jinja2 | Flask injects `session` into template context automatically; avoids needing to pass it through every route |
| Teammate code never modified | All additions marked with `# Added by Mitul` comments; only new lines inserted, nothing removed or changed |
