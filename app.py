from flask import Flask, render_template, request
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# SQLite setup
conn = sqlite3.connect('hazards.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    event TEXT,
    city TEXT,
    lang TEXT,
    filename TEXT
)
''')
conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text_input = request.form.get("text")
        event_input = request.form.get("event")
        city_input = request.form.get("city")
        lang_input = request.form.get("lang")
        file_input = request.files.get("file")
        filename = None
        if file_input:
            filename = file_input.filename
            file_input.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor.execute("""
            INSERT INTO submissions (text, event, city, lang, filename)
            VALUES (?, ?, ?, ?, ?)
        """, (text_input, event_input, city_input, lang_input, filename))
        conn.commit()

    cursor.execute("SELECT * FROM submissions ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    submissions = [
        dict(
            id=r[0],
            text=r[1],
            event=r[2],
            city=r[3],
            lang=r[4],
            filename=r[5]
        )
        for r in rows
    ]

    return render_template("index.html", submissions=submissions)

if __name__ == "__main__":
    app.run(debug=True)
