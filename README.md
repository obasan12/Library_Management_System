# Library Management System

A web-based Library Management System designed to streamline book borrowing and returning processes in libraries. This system allows users to register, log in, borrow, and return books efficiently while helping admins manage the book inventory.

## Features

- **User Registration and Login**: Users can create accounts, log in, and access their personalized dashboards.
- **Book Management**: Users can browse the list of available books and borrow or return books.
- **Admin Dashboard**: Admins can manage the library's book collection, adding or removing books from the system.
- **Real-Time Book Availability**: The system displays available books for borrowing and ensures no book can be borrowed if no copies are available.

## Why Adopt This Tool?

This Library Management System can significantly improve the efficiency and organization of library operations. It provides a user-friendly interface for both the staff and library members. By automating the process of managing books, users can save time and minimize human error. It also enhances accessibility for library users by enabling them to browse, borrow, and return books remotely.

## Installation Instructions

1. **Clone the Repository**:

    ```
    https://github.com/obasan12/Library_Management_System.git
    cd Library-Management-System
    ```

2. **Set up a Virtual Environment** :

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:

    Make sure you have Python 3.x installed, then install the required packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the Database**:

    Run the following command to set up your database:

    ```bash
    flask db upgrade
    ```

    This will create the necessary tables in your database.

5. **Run the Application**:

    Start the Flask development server:

    ```bash
    flask run
    ```

    The app will be accessible at `http://127.0.0.1:5000/`.

## Usage

- **User**: Register for an account, log in, browse books, borrow, and return books.
- **Admin**: Log in with admin credentials to manage the book collection (add/remove books).

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (with Flask-SQLAlchemy)
- **Authentication**: Flask-Login, Flask-WTF

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions, feel free to reach out to me at emerickcipher@gmail.com.
Thanks
