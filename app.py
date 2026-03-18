from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Get DATABASE URL from Render
DATABASE_URL = os.environ.get("DATABASE_URL")

# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Create table if not exists
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT,
        project TEXT,
        message TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Run once when app starts
init_db()

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Form submit
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    project = request.form['project']
    message = request.form['message']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contacts (name, email, phone, project, message) VALUES (%s, %s, %s, %s, %s)",
        (name, email, phone, project, message)
    )

    conn.commit()
    conn.close()

    return "✅ Message Saved Successfully!"

# View all data
@app.route('/data')
def view_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    html = "<h1>📩 User Messages</h1>"

    for row in rows:
        html += f"""
        <div style='border:1px solid black; padding:10px; margin:10px;'>
            <p><b>Name:</b> {row[1]}</p>
            <p><b>Email:</b> {row[2]}</p>
            <p><b>Phone:</b> {row[3]}</p>
            <p><b>Project:</b> {row[4]}</p>
            <p><b>Message:</b> {row[5]}</p>
        </div>
        """

    return html

if __name__ == '__main__':
    app.run(debug=True)
