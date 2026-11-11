
import sqlite3
from student import Student
from course import Course
from Enrollment import Enrollment

conn = sqlite3.connect("classone.dp.db")
cursor = conn.cursor()

print("STUDENT MANAGEMENT SYSTEM")
print("1. Add Student")
print("2. Show All Students")
print("3. Add Course")
print("4. Show All Courses")
print("5. Enroll Student")
print("6. Show All Enrollments")

choice = input("Enter your choice: ")

if choice == "1":
    first = input("First Name: ")
    last = input("Last Name: ")
    email = input("Email: ")

    student = Student(first, last, email)

    cursor.execute(
        "INSERT INTO Students (FirstName, LastName, Email) VALUES (?, ?, ?)",
        (student.first_name, student.last_name, student.email)
    )

    conn.commit()
    print("Student added successfully!")

elif choice == "2":
    cursor.execute("SELECT * FROM Students")

    for student in cursor.fetchall():
        print(student)

elif choice == "3":
    code = input("Course Code: ")
    credits = int(input("Credits: "))

    course = Course(code, credits)

    cursor.execute(
        "INSERT INTO Courses (CourseCode, Credits) VALUES (?, ?)",
        (course.course_code, course.credits)
    )

    conn.commit()
    print("Course added successfully!")

elif choice == "4":
    cursor.execute("SELECT * FROM Courses")

    for course in cursor.fetchall():
        print(course)

elif choice == "5":
    student_id = int(input("Student ID: "))
    course_id = int(input("Course ID: "))
    date = input("Registration Date (YYYY-MM-DD): ")

    enrollment = Enrollment(student_id, course_id, date)

    cursor.execute(
        "INSERT INTO Enrollments (StudentID, CourseID, RegistrationDate) VALUES (?, ?, ?)",
        (enrollment.student_id, enrollment.course_id, enrollment.registration_date)
    )

    conn.commit()
    print("Student enrolled successfully!")

elif choice == "6":
    cursor.execute("SELECT * FROM Enrollments")

    for enrollment in cursor.fetchall():
        print(enrollment)


conn.close()
