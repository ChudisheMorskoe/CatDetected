import sqlite3
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'BazYa'


def create_connection():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    return conn, cursor


def close_connection(conn):
    conn.close()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    error_message = None
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            if not username:
                error_message = "Must provide username"
                return render_template('login.html', error_message=error_message)
            elif not password:
                error_message = "Must provide password"
                return render_template('login.html', error_message=error_message)

            conn, cursor = create_connection()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            close_connection(conn)

            if not user or not check_password_hash(user[2], password):
                error_message = "Invalid username and/or password"
                return render_template('login.html', error_message=error_message)

            session["user_id"] = user[0]
            flash("Logged in successfully", "success")
            return redirect(url_for('index'))
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html', error_message=error_message)


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return "Необходимо указать имя пользователя", 400
        elif not password:
            return "Необходимо указать пароль", 400
        elif not confirmation:
            return "Необходимо подтвердить пароль", 400
        elif password != confirmation:
            return "Пароли не совпадают", 400

        conn, cursor = create_connection()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            close_connection(conn)
            return "Имя пользователя уже существует", 400

        password_hash = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        new_user = cursor.fetchone()
        close_connection(conn)

        session["user_id"] = new_user[0]
        return redirect("/")
    else:
        return render_template("register.html")


@app.route('/detected')
@login_required
def detected():
    return render_template('detected.html')


if __name__ == "__main__":
    app.run(debug=True)
