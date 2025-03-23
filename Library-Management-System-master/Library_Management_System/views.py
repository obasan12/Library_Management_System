from datetime import datetime
from functools import wraps

from flask import flash, redirect, render_template, request, url_for
from flask.blueprints import Blueprint
from flask.views import MethodView
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager
from .models import Book, User  # Ensure Copy model is not needed here if not used

main = Blueprint("main", __name__)

def requires_admin(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.admin:
            flash("Admin access required!")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return wrapped

@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)

@main.route("/", methods=["GET"])
def index():
    books = Book.query.all()
    return render_template("index.html", year=datetime.now().year, books=books if books else "No books are in the library!")

@main.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", year=datetime.now().year)

class LoginView(MethodView):
    def get(self):
        return render_template("login.html", year=datetime.now().year)

    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(request.args.get("next") or url_for("main.dashboard"))
        flash("Invalid Credentials!")
        return redirect(url_for("main.login"))

class RegisterView(MethodView):
    def get(self):
        return render_template("register.html", year=datetime.now().year)

    def post(self):
        name = request.form.get("name")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"), method="pbkdf2:sha256")

        if User.query.filter_by(email=email).first():
            flash("User already exists!")
            return redirect(url_for("main.register"))

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(request.args.get("next") or url_for("main.dashboard"))

class AdminView(MethodView):
    def get(self):
        return render_template("admin.html", year=datetime.now().year)

    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, admin=True).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.admin_dashboard"))

        flash("Invalid Credentials!")
        return redirect(url_for("main.admin"))

@main.route("/admin/dashboard", methods=["GET"])
@login_required
@requires_admin
def admin_dashboard():
    books = Book.query.all()
    return render_template("admin_dashboard.html", books=books, year=datetime.now().year)

class AddBookView(MethodView):
    def get(self):
        return render_template("add_book.html", year=datetime.now().year)

    def post(self):
        name = request.form.get("name")
        author = request.form.get("author")
        description = request.form.get("description")
        number = int(request.form.get("number"))

        book = Book.query.filter_by(name=name).first()
        if book:
            flash("Book already exists!")
            return redirect(url_for("main.add_book"))

        book = Book(
            name=name,
            author=author,
            description=description,
            total_copy=number,
            present_copy=number,
            issued_copy=0,
        )

        db.session.add(book)
        db.session.commit()
        flash("Book added successfully!")
        return redirect(url_for("main.admin_dashboard"))

class RemoveBookView(MethodView):
    def get(self):
        books = Book.query.all()
        return render_template("remove_book.html", books=books, year=datetime.now().year)

    def post(self):
        book_id = request.form.get("book")
        book = Book.query.filter_by(id=book_id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            flash("Book removed successfully!")
        else:
            flash("Book not found!")
        return redirect(url_for("main.admin_dashboard"))

@main.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully!")
    return redirect(url_for("main.login"))

# Register the routes for views
main.add_url_rule("/register", view_func=RegisterView.as_view("register"))
main.add_url_rule("/login", view_func=LoginView.as_view("login"))
main.add_url_rule("/admin", view_func=AdminView.as_view("admin"))
main.add_url_rule("/add/book", view_func=login_required(requires_admin(AddBookView.as_view("add_book"))))
main.add_url_rule("/remove/book", view_func=login_required(requires_admin(RemoveBookView.as_view("remove_book"))))




@main.route("/issue/book", methods=["GET", "POST"])
@login_required
def issue_book():
    if request.method == "POST":
        # Handle book issue logic here
        book_id = request.form.get('book')
        # Additional logic to issue the book
        flash("Book issued successfully!")
        return redirect(url_for("main.dashboard"))
    
    # Fetch books and render the form
    books = Book.query.all()
    return render_template("issue.html", books=books)



@main.route("/return/book", methods=["GET", "POST"])
@login_required
def return_book():
    if request.method == "POST":
        book_id = request.form.get("book")
        book = Book.query.get(book_id)
        
        # Check if the book exists and is issued to the current user
        if book and book in current_user.books:
            # Remove the book from the user's list
            current_user.books.remove(book)
            # Increment the available copies of the book
            book.present_copy += 1
            db.session.commit()
            flash("Book returned successfully!")
        else:
            flash("You cannot return this book!")
        
        return redirect(url_for("main.dashboard"))

    # For GET requests, display the return book form
    books = Book.query.filter(Book in current_user.books).all()
    return render_template("return.html", books=books)
