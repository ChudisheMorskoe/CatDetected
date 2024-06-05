import os
import uuid

import cv2
import sqlite3
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory
from moviepy.video.io.VideoFileClip import VideoFileClip
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from ssd import process_image

UPLOAD_FOLDER = 'static/img/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'bmp'}

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1000 * 1000
app.secret_key = 'BazYa'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/download_processed/<filename>')
def download_processed_file(filename):
    try:
        return send_from_directory('', filename, as_attachment=True)
    finally:
        # after download file - delete
        file_path = os.path.join('', filename)
        if os.path.exists(file_path):
            os.remove(file_path)


# check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                img = cv2.imread(file_path)
                processed_img = process_image(img)
                if processed_img is not None:
                    output_filename = f"processed_image_{uuid.uuid4()}.jpg"
                    cv2.imwrite(os.path.join(os.getcwd(), output_filename), processed_img)
                    return redirect(url_for('download_processed_file', filename=output_filename))
                else:
                    flash('Unsupported file format')
                    return redirect(request.url)
            elif filename.lower().endswith('.mp4'):
                clip = VideoFileClip(file_path)
                out_path = f'processed_video_{uuid.uuid4()}.mp4'
                processed_clip = clip.fl_image(process_image)
                processed_clip.write_videofile(os.path.join(os.getcwd(), out_path), audio=True)
                return redirect(url_for('download_processed_file', filename=out_path))
            else:
                flash('Unsupported file format')
                return redirect(request.url)
    return render_template('upload.html')


@app.route('/download_processed/<filename>')
def download_file(filename):
    return send_from_directory('', filename, as_attachment=True)


def create_connection():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    return conn, cursor


def close_connection(conn):
    conn.close()


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
            return "It is necessary to specify the user name", 400
        elif not password:
            return "You need to specify a password", 400
        elif not confirmation:
            return "You need to confirm the password", 400
        elif password != confirmation:
            return "passwords doesnt match", 400

        conn, cursor = create_connection()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            close_connection(conn)
            return "This username already ude ", 400

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


if __name__ == "__main__":
    app.run(debug=True)
