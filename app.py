import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "professional_portal_key"

# --- 1. DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Create Teachers Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS teachers 
                      (id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT)''')
    # Create Students Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS students 
                      (id INTEGER PRIMARY KEY, name TEXT, roll_no TEXT UNIQUE, password TEXT,
                       eng INTEGER, sl INTEGER, mat INTEGER, sci INTEGER, soc INTEGER,
                       total INTEGER, percent REAL, grade TEXT, result TEXT, teacher_id INTEGER)''')
    
    # Predefined Teacher Accounts
    teachers = [('sushanth', 'sushanth07', 'Sushanth'),
                ('praneetha', 'praneetha07', 'Praneetha'),
                ('aparna', 'aparna07', 'Aparna')]
    for username, pwd, name in teachers:
        cursor.execute("SELECT * FROM teachers WHERE username=?", (username,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO teachers (username, password, name) VALUES (?, ?, ?)", (username, pwd, name))
    conn.commit()
    conn.close()

# --- 2. AUTOMATIC RESULT LOGIC ---
def process_marks(marks):
    total = sum(marks)
    percent = total / 5
    # Overall Result: If any subject is below 35, the student fails the year
    overall = "PASS" if all(m >= 35 for m in marks) else "FAIL"
    
    if percent >= 90: grade = "A"
    elif percent >= 75: grade = "B"
    elif percent >= 60: grade = "C"
    else: grade = "D"
    
    return total, percent, grade, overall

# --- 3. ROUTES (THE PAGES) ---
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/teacher/login', methods=['POST'])
def teacher_login():
    user, pwd = request.form['username'], request.form['password']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers WHERE username=? AND password=?", (user, pwd))
    teacher = cursor.fetchone()
    conn.close()
    if teacher:
        session['teacher_id'], session['teacher_name'] = teacher[0], teacher[3]
        return redirect(url_for('admin_dashboard'))
    return "Invalid Teacher Credentials"

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'teacher_id' not in session: return redirect('/')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE teacher_id=?", (session['teacher_id'],))
    students = cursor.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', students=students, t_name=session['teacher_name'])

@app.route('/add_student', methods=['POST'])
def add_student():
    if 'teacher_id' not in session: return redirect('/')
    d = request.form
    marks = [int(d['eng']), int(d['sl']), int(d['mat']), int(d['sci']), int(d['soc'])]
    total, percent, grade, result = process_marks(marks)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO students (name, roll_no, password, eng, sl, mat, sci, soc, total, percent, grade, result, teacher_id) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                       (d['name'], d['roll_no'], d['roll_no'], *marks, total, percent, grade, result, session['teacher_id']))
        conn.commit()
    except: flash("Roll number already exists!")
    conn.close()
    return redirect(url_for('admin_dashboard'))

# --- NEW: DELETE STUDENT ---
@app.route('/delete_student/<int:id>')
def delete_student(id):
    if 'teacher_id' not in session: return redirect('/')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=? AND teacher_id=?", (id, session['teacher_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/student/login_page')
def student_login_page(): return render_template('student_login.html')

@app.route('/student/login', methods=['POST'])
def student_login():
    roll, pwd = request.form['roll_no'], request.form['password']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE roll_no=? AND password=?", (roll, pwd))
    student = cursor.fetchone()
    conn.close()
    if student:
        session['student_id'] = student[0]
        return redirect(url_for('student_dashboard'))
    return "Invalid Student Login"

@app.route('/student_dashboard')
def student_dashboard():
    if 'student_id' not in session: return redirect('/')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (session['student_id'],))
    student = cursor.fetchone()
    conn.close()
    return render_template('student_dashboard.html', s=student)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)