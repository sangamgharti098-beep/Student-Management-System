

from flask import Flask, request, redirect
import sqlite3
from student import Student
from course import Course
from Enrollment import Enrollment

app = Flask(__name__)

DATABASE = "classone.dp.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        action = request.form.get("action")

        try:
            conn = get_connection()

            if action == "student":
                student = Student(
                    request.form["first"],
                    request.form["last"],
                    request.form["email"]
                )

                conn.execute(
                    "INSERT INTO Students (FirstName, LastName, Email) VALUES (?, ?, ?)",
                    (student.first_name, student.last_name, student.email)
                )
                message = "Student added successfully!"

            elif action == "course":
                course = Course(
                    request.form["code"],
                    int(request.form["credits"])
                )

                conn.execute(
                    "INSERT INTO Courses (CourseCode, Credits) VALUES (?, ?)",
                    (course.course_code, course.credits)
                )
                message = "Course added successfully!"

            elif action == "enrollment":
                enrollment = Enrollment(
                    int(request.form["student_id"]),
                    int(request.form["course_id"]),
                    request.form["date"]
                )

                conn.execute(
                    "INSERT INTO Enrollments (StudentID, CourseID, RegistrationDate) VALUES (?, ?, ?)",
                    (enrollment.student_id,
                     enrollment.course_id,
                     enrollment.registration_date)
                )
                message = "Student enrolled successfully!"

            conn.commit()
            conn.close()

        except (sqlite3.Error, ValueError) as error:
            message = "Error: " + str(error)

    conn = get_connection()

    students = conn.execute(
        "SELECT * FROM Students"
    ).fetchall()

    courses = conn.execute(
        "SELECT * FROM Courses"
    ).fetchall()

    enrollments = conn.execute("""
        SELECT e.EnrollmentID,
               s.FirstName || ' ' || s.LastName,
               c.CourseCode,
               e.RegistrationDate
        FROM Enrollments e
        LEFT JOIN Students s ON e.StudentID = s.StudentID
        LEFT JOIN Courses c ON e.CourseID = c.CourseID
    """).fetchall()

    conn.close()

    def make_table(headers, rows):
        html = "<table border='1' cellpadding='10'>"
        html += "<tr>"
        for heading in headers:
            html += "<th>" + heading + "</th>"
        html += "</tr>"

        from html import escape
        for row in rows:
            html += "<tr>"
            for value in row:
                html += "<td>" + escape(str(value)) + "</td>"
            html += "</tr>"

        html += "</table>"
        return html

    student_table = make_table(
        ["ID", "First Name", "Last Name", "Email"],
        students
    )

    course_table = make_table(
        ["ID", "Course Code", "Credits"],
        courses
    )

    enrollment_table = make_table(
        ["ID", "Student", "Course", "Date"],
        enrollments
    )

    from html import escape
    safe_message = escape(message)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Management System</title>
        <style>
            body {{
                font-family: Arial;
                background: #f4f6f9;
                margin: 30px;
            }}
            h1 {{
                color: #23395d;
                text-align: center;
            }}
            .section {{
                background: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 8px;
            }}
            input {{
                padding: 10px;
                margin: 5px;
            }}
            button {{
                padding: 10px 20px;
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-top: 10px;
            }}
            th {{
                background: #dbeafe;
            }}
            td, th {{
                text-align: left;
            }}
        </style>
    </head>
    <body>

    <h1>Student Management System</h1>

    <p>{safe_message}</p>

    <div class="section">
        <h2>1. Add Student</h2>
        <form method="POST">
            <input type="hidden" name="action" value="student">
            <input name="first" placeholder="First Name" required>
            <input name="last" placeholder="Last Name" required>
            <input name="email" type="email"
                   placeholder="Email" required>
            <button type="submit">Add Student</button>
        </form>
    </div>

    <div class="section">
        <h2>2. Show All Students</h2>
        {student_table}
    </div>

    <div class="section">
        <h2>3. Add Course</h2>
        <form method="POST">
            <input type="hidden" name="action" value="course">
            <input name="code" placeholder="Course Code" required>
            <input name="credits" type="number" min="1"
                   placeholder="Credits" required>
            <button type="submit">Add Course</button>
        </form>
    </div>

    <div class="section">
        <h2>4. Show All Courses</h2>
        {course_table}
    </div>

    <div class="section">
        <h2>5. Enroll Student</h2>
        <form method="POST">
            <input type="hidden" name="action" value="enrollment">
            <input name="student_id" type="number"
                   placeholder="Student ID" required>
            <input name="course_id" type="number"
                   placeholder="Course ID" required>
            <input name="date" type="date" required>
            <button type="submit">Enroll Student</button>
        </form>
    </div>

    <div class="section">
        <h2>6. Show All Enrollments</h2>
        {enrollment_table}
    </div>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
