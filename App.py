# app.py
# Favourite Books — Area 2: Browse Catalogue & Search Books

from flask import Flask, render_template, request, jsonify
from flask import session, redirect, url_for  
from catalogue import Catalogue, CatalogueManager
from data import seed_catalogue
from customer import Customer  
from order import OrderManager
from shopping_cart import ShoppingCart

app = Flask(__name__)
app.secret_key = 'bookstore-secret-2026'  

# Bootstrap: creates catalogue, loads data, wraps in manager
catalogue = Catalogue()
seed_catalogue(catalogue)
manager = CatalogueManager(catalogue)
order_manager = OrderManager(manager)
carts = {}


def get_cart(customer_id="guest"):
    if customer_id not in carts:
        carts[customer_id] = ShoppingCart(customer_id, manager)
    carts[customer_id].remove_expired_items()
    return carts[customer_id]

# Added by Dan: Aread 1 For Browse Catalogue
@app.route("/")
def index():
    categories = manager.get_all_categories()
    return render_template("index.html", categories=categories)


@app.route("/search")
def search():
    query    = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    if query:
        books = manager.search_books(query)
    else:
        books = manager.get_all_books()

    if category:
        books = [b for b in books if b.category.category_id == category]

    return jsonify([b.to_dict() for b in books])


@app.route("/book/<book_id>")
def book_detail(book_id):
    book = manager.get_book_by_id(book_id)
    if not book:
        return "Book not found", 404
    return render_template("book_detail.html", book=book.to_dict())

# Added by Mun — Area 3: Manage Shopping Cart
@app.route("/cart")
def cart_page():
    cart = get_cart()
    items = cart.get_display_items()
    subtotal = cart.calculate_total()
    shipping = 4.99 if items else 0.00
    return render_template(
        "cart.html",
        items=items,
        subtotal=subtotal,
        shipping=shipping,
        total=subtotal + shipping,
        error=request.args.get("error")
    )


@app.route("/cart/add", methods=["POST"])
def cart_add():
    cart = get_cart()
    try:
        cart.add_item(
            request.form.get("book_id", ""),
            request.form.get("quantity", "1")
        )
    except ValueError as exc:
        return redirect(url_for("cart_page", error=str(exc)))
    return redirect(url_for("cart_page"))


@app.route("/cart/remove", methods=["POST"])
def cart_remove():
    cart = get_cart()
    try:
        cart.remove_item(request.form.get("book_id", ""))
    except ValueError as exc:
        return redirect(url_for("cart_page", error=str(exc)))
    return redirect(url_for("cart_page"))


@app.route("/cart/update", methods=["POST"])
def cart_update():
    cart = get_cart()
    try:
        cart.update_quantity(
            request.form.get("book_id", ""),
            request.form.get("quantity", "1")
        )
    except ValueError as exc:
        return redirect(url_for("cart_page", error=str(exc)))
    return redirect(url_for("cart_page"))

# Added by Alex — Area 4: Place Order & Invoice
@app.route("/cart/checkout", methods=["POST"])
def cart_checkout():
    cart = get_cart()
    try:
        order, invoice = order_manager.place_order_from_items(
            customer_name=request.form.get("customer_name", ""),
            delivery_address=request.form.get("delivery_address", ""),
            checkout_items=cart.checkout_items()
        )
        cart.clear_cart()
        return render_template("invoice.html", invoice=invoice.to_dict())
    except ValueError as exc:
        return redirect(url_for("cart_page", error=str(exc)))


@app.route("/order/<book_id>", methods=["GET", "POST"])
def place_order(book_id):
    # Route for order placement and invoice generation.
    book = manager.get_book_by_id(book_id)
    if not book:
        return "Book not found", 404

    error = None
    if request.method == "POST":
        try:
            order, invoice = order_manager.place_order(
                customer_name=request.form.get("customer_name", ""),
                delivery_address=request.form.get("delivery_address", ""),
                book_id=book_id,
                quantity=request.form.get("quantity", "1")
            )
            return render_template("invoice.html", invoice=invoice.to_dict())
        except ValueError as exc:
            error = str(exc)

    return render_template("order_form.html", book=book.to_dict(), error=error)

# Added by Mitul — Area 1: Customer Account


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', error=None, form={})

    first_name       = request.form.get('first_name', '').strip()
    last_name        = request.form.get('last_name', '').strip()
    email            = request.form.get('email', '').strip()
    phone            = request.form.get('phone', '').strip()
    password         = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    form_data = {'first_name': first_name, 'last_name': last_name,
                 'email': email, 'phone': phone}

    if not all([first_name, last_name, email, phone, password, confirm_password]):
        return render_template('register.html', error='All fields are required.', form=form_data)
    if password != confirm_password:
        return render_template('register.html', error='Passwords do not match.', form=form_data)
    if len(password) < 6:
        return render_template('register.html', error='Password must be at least 6 characters.', form=form_data)
    if Customer.email_exists(email):
        return render_template('register.html', error='An account with that email already exists.', form=form_data)

    customer = Customer(first_name, last_name, email, phone, Customer.hash_password(password))
    customer.save()
    session['customer_email'] = customer.email
    session['customer_name']  = customer.first_name
    return redirect(url_for('account'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', error=None, success=None)

    email    = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    customer = Customer.find_by_email(email)
    if not customer or not customer.check_password(password):
        return render_template('login.html', error='Invalid email or password.', success=None)

    session['customer_email'] = customer.email
    session['customer_name']  = customer.first_name
    return redirect(url_for('account'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/account')
def account():
    if 'customer_email' not in session:
        return redirect(url_for('login'))
    customer = Customer.find_by_email(session['customer_email'])
    if not customer:
        session.clear()
        return redirect(url_for('login'))
    return render_template('account.html', customer=customer)


if __name__ == "__main__":
    app.run(debug=True)