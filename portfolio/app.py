from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        project TEXT,
        message TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    project = request.form['project']
    message = request.form['message']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contacts (name, email, phone, project, message) VALUES (?, ?, ?, ?, ?)",
        (name, email, phone, project, message)
    )

    conn.commit()
    conn.close()

    return "✅ Message Saved Successfully!"

if __name__ == '__main__':
    app.run(debug=True)