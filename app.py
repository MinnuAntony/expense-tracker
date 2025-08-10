from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "expenses.db"

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# HTML Template
html = """
<!doctype html>
<html>
<head>
    <title>Expense Tracker</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="p-4">

<div class="container">
    <h1 class="mb-4">Expense Tracker</h1>

    <h3>Total Expenses: ₹{{ total }}</h3>

    <table class="table table-bordered mt-3">
        <thead class="table-dark">
            <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Amount (₹)</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
        {% for expense in expenses %}
            <tr>
                <td>{{ expense[1] }}</td>
                <td>{{ expense[2] }}</td>
                <td>{{ expense[3] }}</td>
                <td>
                    <a href="/edit/{{ expense[0] }}" class="btn btn-sm btn-warning">Edit</a>
                    <a href="/delete/{{ expense[0] }}" class="btn btn-sm btn-danger">Delete</a>
                </td>
            </tr>
        {% endfor %}
        </tbody>
    </table>

    <h2 class="mt-4">Add New Expense</h2>
    <form method="post" action="/add" class="row g-3">
        <div class="col-md-3">
            <input type="date" name="date" class="form-control" required>
        </div>
        <div class="col-md-4">
            <input type="text" name="description" placeholder="Description" class="form-control" required>
        </div>
        <div class="col-md-3">
            <input type="number" name="amount" placeholder="Amount" class="form-control" required>
        </div>
        <div class="col-md-2">
            <button type="submit" class="btn btn-primary w-100">Add</button>
        </div>
    </form>
</div>

</body>
</html>
"""

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    total = sum(exp[3] for exp in expenses)
    conn.close()
    return render_template_string(html, expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    description = request.form['description']
    amount = float(request.form['amount'])

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, description, amount) VALUES (?, ?, ?)",
                   (date, description, amount))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        amount = float(request.form['amount'])
        cursor.execute("UPDATE expenses SET date=?, description=?, amount=? WHERE id=?",
                       (date, description, amount, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM expenses WHERE id=?", (id,))
    expense = cursor.fetchone()
    conn.close()

    return f"""
    <h2>Edit Expense</h2>
    <form method="post">
        Date: <input type="date" name="date" value="{expense[1]}" required><br><br>
        Description: <input type="text" name="description" value="{expense[2]}" required><br><br>
        Amount: <input type="number" name="amount" value="{expense[3]}" required><br><br>
        <input type="submit" value="Update Expense">
    </form>
    """

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)