"""
================================================================================
STUDENT RECORD MANAGEMENT SYSTEM USING XML
Flask Web Application (app.py)

Provides a modern web interface for the Student Record Management System.
Backend: Python 3.x + Flask
Data Storage: students.xml (via xml.etree.ElementTree)
Schema Validation: students.xsd (via lxml, optional)
================================================================================
"""

import os
import sys

# Ensure project root is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from modules.student_operations import (
    get_all_students,
    find_student_by_id,
    add_student,
    update_student,
    delete_student,
    get_summary_stats,
)
from modules.validation import sanitize_input

# ------------------------------------------------------------------ Flask App
app = Flask(__name__)
app.secret_key = "student_record_xml_secret_key_2024"


# ============================================================ DASHBOARD
@app.route("/")
def dashboard():
    """Display the system dashboard with summary statistics."""
    stats = get_summary_stats()
    return render_template("dashboard.html", stats=stats)


# ============================================================ ADD STUDENT
@app.route("/add", methods=["GET", "POST"])
def add_student_page():
    """Render the Add Student form and handle submission."""
    if request.method == "POST":
        student_id = sanitize_input(request.form.get("student_id"))
        name = sanitize_input(request.form.get("name"))
        course = sanitize_input(request.form.get("course"))
        semester = sanitize_input(request.form.get("semester"))

        success, message = add_student(student_id, name, course, semester)
        if success:
            flash(message, "success")
            return redirect(url_for("view_students_page"))
        else:
            flash(message, "danger")

    return render_template("add_student.html")


# ============================================================ VIEW STUDENTS
@app.route("/view")
def view_students_page():
    """Display all student records in a table."""
    students = get_all_students()
    return render_template("view_students.html", students=students)


# ============================================================ SEARCH STUDENT
@app.route("/search", methods=["GET", "POST"])
def search_student_page():
    """Search for a student by ID."""
    student = None
    searched = False

    if request.method == "POST":
        student_id = sanitize_input(request.form.get("student_id"))
        searched = True
        if student_id:
            student = find_student_by_id(student_id)
            if student is None:
                flash(f"Student with ID '{student_id}' not found.", "warning")
        else:
            flash("Please enter a Student ID to search.", "danger")

    return render_template("search_student.html", student=student, searched=searched)


# ============================================================ UPDATE STUDENT
@app.route("/update", methods=["GET", "POST"])
def update_student_page():
    """Update a student's information."""
    student = None

    if request.method == "POST":
        action = request.form.get("action")
        student_id = sanitize_input(request.form.get("student_id"))

        if action == "find":
            # Step 1: Find the student and show the update form
            if student_id:
                student = find_student_by_id(student_id)
                if student is None:
                    flash(f"Student with ID '{student_id}' not found.", "warning")
            else:
                flash("Please enter a Student ID.", "danger")

        elif action == "update":
            # Step 2: Save the updated details
            name = sanitize_input(request.form.get("name"))
            course = sanitize_input(request.form.get("course"))
            semester = sanitize_input(request.form.get("semester"))

            success, message, updated = update_student(
                student_id,
                name if name else None,
                course if course else None,
                semester if semester else None,
            )

            if success:
                flash(message, "success")
                return redirect(url_for("view_students_page"))
            else:
                flash(message, "danger")
                student = find_student_by_id(student_id)

    return render_template("update_student.html", student=student)


# ============================================================ DELETE STUDENT
@app.route("/delete", methods=["GET", "POST"])
def delete_student_page():
    """Delete a student record after confirmation."""
    student = None

    if request.method == "POST":
        action = request.form.get("action")
        student_id = sanitize_input(request.form.get("student_id"))

        if action == "find":
            if student_id:
                student = find_student_by_id(student_id)
                if student is None:
                    flash(f"Student with ID '{student_id}' not found.", "warning")
            else:
                flash("Please enter a Student ID.", "danger")

        elif action == "delete":
            success, message = delete_student(student_id)
            if success:
                flash(message, "success")
                return redirect(url_for("view_students_page"))
            else:
                flash(message, "danger")

    return render_template("delete_student.html", student=student)


# ============================================================ INLINE EDIT & DELETE (AJAX)
@app.route("/api/delete/<student_id>", methods=["DELETE"])
def api_delete_student(student_id):
    """API endpoint to delete a student (used by the View Students table)."""
    clean_id = sanitize_input(student_id)
    success, message = delete_student(clean_id)
    return jsonify({"success": success, "message": message})


@app.route("/api/student/<student_id>", methods=["GET"])
def api_get_student(student_id):
    """API endpoint to fetch a single student record by ID."""
    clean_id = sanitize_input(student_id)
    student = find_student_by_id(clean_id)
    if student:
        return jsonify({"success": True, "student": student})
    return jsonify({"success": False, "message": "Student not found."}), 404


@app.route("/api/update", methods=["POST"])
def api_update_student():
    """API endpoint to update a student record (used by inline editing)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400

    student_id = sanitize_input(data.get("student_id", ""))
    name = sanitize_input(data.get("name", ""))
    course = sanitize_input(data.get("course", ""))
    semester = sanitize_input(data.get("semester", ""))

    success, message, updated = update_student(
        student_id,
        name if name else None,
        course if course else None,
        semester if semester else None,
    )
    return jsonify({"success": success, "message": message, "student": updated})


# ============================================================ RUN
if __name__ == "__main__":
    print("=" * 60)
    print("  STUDENT RECORD MANAGEMENT SYSTEM USING XML")
    print("  Open your browser at: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host="127.0.0.1", port=5000)
