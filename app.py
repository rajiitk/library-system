import sys
sys.path.append("/users/mme/mt/rajkyadav25/Documents/library-system/libs/usr/lib/python3/dist-packages")

from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import os

app = Flask(__name__)

# Absolute path for DB file
DB_PATH = "/users/mme/mt/rajkyadav25/Documents/library-system/library.db"

# ---------- Create DB if not exists ----------
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                section TEXT,
                shelf TEXT
            )
        """)
        conn.commit()
        conn.close()

# ---------- Homepage ----------
@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return render_template("index.html", books=books)

# ---------- Add Book ----------
@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        section = request.form["section"]
        shelf = request.form["shelf"]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO books (title, author, section, shelf) VALUES (?,?,?,?)",
                  (title, author, section, shelf))
        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("add_book.html")

# ---------- Delete ----------
@app.route("/delete/<int:book_id>")
def delete(book_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    return redirect("/")

# ---------- CSV Export ----------
@app.route("/export")
def export_csv():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    rows = c.fetchall()
    conn.close()

    csv_path = "/users/mme/mt/rajkyadav25/Documents/library-system/books.csv"
    with open(csv_path, "w") as f:
        f.write("ID,Title,Author,Section,Shelf\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")

    return send_file(csv_path, as_attachment=True)

# ---------- Run Server ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
