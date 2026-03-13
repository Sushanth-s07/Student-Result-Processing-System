# Student Result Processing System

## Project Overview
The Student Result Processing System is a web application designed to manage and process student academic results efficiently. The system allows administrators (teachers) to add, update, and manage student marks, while students can securely log in to view their results.

The application automatically calculates total marks, percentage, and grades. It also provides graphical result analysis using charts.

## Technology Stack

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python (Flask Framework)

Database:
- SQLite

Data Visualization:
- Chart.js

## Features

- Admin login authentication
- Teachers can add and update student marks
- Students can log in and view their results
- Automatic total marks calculation
- Automatic percentage calculation
- Grade generation using conditional logic
- Graphical result analysis using charts
- Secure data storage using SQLite database
- Clean and user-friendly interface

## Project Structure

student-result-system/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
│   └── database.db
│
├── models/
│   └── db.py
│
├── routes/
│   ├── auth_routes.py
│   ├── student_routes.py
│   └── result_routes.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── add_student.html
│   ├── add_result.html
│   ├── view_results.html
│   └── analytics.html
│
├── static/
│   │
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   ├── script.js
│   │   └── charts.js
│   │
│   └── images/
│       └── logo.png
│
└── utils/
    └── helpers.py


## How to Run Locally

1️⃣ Clone the Repository

Open Command Prompt / Terminal and run:
git clone https://github.com/Sushanth-s07/Student-Result-Processing-System

2️⃣ Navigate to the Project Folder
cd student-result-system

3️⃣ Install Required Dependencies

Make sure Python is installed. Then run:

pip install -r requirements.txt

This will install required libraries such as:

Flask

SQLite (built-in with Python)

4️⃣ Verify Project Structure

Ensure your folder contains:

app.py
requirements.txt
templates/
static/
database/

5️⃣ Run the Flask Application

Start the server by running:

python app.py

6️⃣ Open the Application in Browser

After running the server, open your browser and go to:

http://127.0.0.1:5000
