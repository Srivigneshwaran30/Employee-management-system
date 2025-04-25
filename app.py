from flask import Flask, render_template, request, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key = 'SRI'

# ---------------- In-Memory Data ----------------
users = {
    "admin1": {"password": "admin123", "role": "admin"},
    "employee1": {"password": "emp123", "role": "employee"}
}

employees = []  # Will contain dictionaries like: {'id': 1, 'name': 'John', 'role': 'Developer', 'department': 'IT'}
next_emp_id = 1

# ---------------- Login ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)
        if user and user["password"] == password:
            session['username'] = username
            session['user_role'] = user["role"]
            flash(f"Logged in as {user['role']}", 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

# ---------------- Logout ----------------
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))
# ---------------- admin panel ----------------

@app.route('/adminpanel')  # ✅ proper spelling and outside the logout function
def admin_panel():
    if session.get('user_role') != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('home'))
    return render_template('adminpanel.html')  # ✅ file name must match



# ---------------- Home ----------------
@app.route('/')
def home():
    if 'user_role' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# ---------------- View Employees ----------------
@app.route('/employees')
def view_employees():
    if 'user_role' not in session:
        return redirect(url_for('login'))
    return render_template('view_employees.html', employees=employees)

# ---------------- Add Employee ----------------
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    global next_emp_id
    if session.get('user_role') != 'admin':
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('view_employees'))

    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        department = request.form['department']
        employees.append({'id': next_emp_id, 'name': name, 'role': role, 'department': department})
        next_emp_id += 1
        flash("Employee added successfully!", "success")
        return redirect(url_for('view_employees'))

    return render_template('add_employee.html')

# ---------------- Edit Employee ----------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    if session.get('user_role') != 'admin':
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('view_employees'))

    employee = next((emp for emp in employees if emp['id'] == id), None)
    if not employee:
        flash("Employee not found", "danger")
        return redirect(url_for('view_employees'))

    if request.method == 'POST':
        employee['name'] = request.form['name']
        employee['role'] = request.form['role']
        employee['department'] = request.form['department']
        flash("Employee updated successfully!", "success")
        return redirect(url_for('view_employees'))

    return render_template('edit_employee.html', employee=employee)

# ---------------- Delete Employee ----------------
@app.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    if session.get('user_role') != 'admin':
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('view_employees'))

    global employees
    employees = [emp for emp in employees if emp['id'] != id]
    flash("Employee deleted successfully!", "success")
    return redirect(url_for('view_employees'))

# ---------------- Signup ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if username in users:
            flash("User already exists!", "danger")
        else:
            users[username] = {"password": password, "role": role}
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for('login'))

    return render_template('signup.html')

# ---------------- Run App ----------------
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
