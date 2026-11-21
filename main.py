"""
================================================================================
STUDENT RECORD MANAGEMENT SYSTEM USING XML
M.Tech Computer Science and Engineering Academic Project
Royal College of Engineering & Technology, Akkikavu
APJ Abdul Kalam Technological University

Author: SNEHA V P (RCE26CS058)
Technology: Python 3.x, xml.etree.ElementTree, XML, XSD
================================================================================
"""

import os
import sys
import xml.etree.ElementTree as ET

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XML_FILE = os.path.join(BASE_DIR, "students.xml")
XSD_FILE = os.path.join(BASE_DIR, "students.xsd")


def load_tree(xml_file: str = XML_FILE):
    """
    Check whether the XML file exists. If it does not exist, create a new XML document
    with an empty <students> root element. Parse the XML file and return the XML tree
    and its root element.
    """
    if not os.path.exists(xml_file):
        root = ET.Element("students")
        tree = ET.ElementTree(root)
        save_tree(tree, xml_file)
        return tree, root

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag != "students":
            raise ValueError("Root element is not <students>")
        return tree, root
    except Exception:
        # Corrupted or malformed file: backup and re-initialize
        backup = f"{xml_file}.bak"
        try:
            if os.path.exists(xml_file):
                os.replace(xml_file, backup)
        except OSError:
            pass
        root = ET.Element("students")
        tree = ET.ElementTree(root)
        save_tree(tree, xml_file)
        return tree, root


def save_tree(tree: ET.ElementTree, xml_file: str = XML_FILE):
    """
    Write the modified XML tree to students.xml using UTF-8 encoding
    and standard XML declaration.
    """
    try:
        ET.indent(tree, space="    ", level=0)
    except AttributeError:
        pass
    tree.write(xml_file, encoding="UTF-8", xml_declaration=True)


def add_student():
    """
    Accept a new student's details, check for empty or duplicate ID,
    create the required XML elements, and save the document.
    """
    tree, root = load_tree()

    student_id = input("Enter student ID: ").strip()
    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    # Check for duplicate ID
    for s in root.findall("student"):
        if s.attrib.get("id", "").strip() == student_id:
            print(f"Error: Student ID '{student_id}' already exists.")
            return

    name = input("Enter student name: ").strip()
    if not name:
        print("Error: Student name cannot be empty.")
        return

    course = input("Enter course: ").strip()
    if not course:
        print("Error: Course cannot be empty.")
        return

    semester = input("Enter semester: ").strip()
    if not semester:
        print("Error: Semester cannot be empty.")
        return

    # Create new student element and child elements
    new_student = ET.Element("student", attrib={"id": student_id})
    elem_name = ET.SubElement(new_student, "name")
    elem_name.text = name

    elem_course = ET.SubElement(new_student, "course")
    elem_course.text = course

    elem_sem = ET.SubElement(new_student, "semester")
    elem_sem.text = semester

    root.append(new_student)
    save_tree(tree)
    print("Student added successfully.")


def view_students():
    """
    Read all student records and display their ID, name, course, and semester.
    """
    _, root = load_tree()
    students = root.findall("student")

    if not students:
        print("No student records found.")
        return

    print("--- STUDENT RECORDS ---")
    for s in students:
        s_id = s.attrib.get("id", "N/A")
        name_elem = s.find("name")
        course_elem = s.find("course")
        sem_elem = s.find("semester")

        name = name_elem.text if name_elem is not None and name_elem.text else "N/A"
        course = course_elem.text if course_elem is not None and course_elem.text else "N/A"
        sem = sem_elem.text if sem_elem is not None and sem_elem.text else "N/A"

        print(f"ID: {s_id} | Name: {name} | Course: {course} | Semester: {sem}")


def search_student():
    """
    Accept an ID and use the XML tree to locate the corresponding student.
    Display the record or a not-found message.
    """
    tree, root = load_tree()
    student_id = input("Enter student ID to search: ").strip()

    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    for s in root.findall("student"):
        if s.attrib.get("id", "").strip() == student_id:
            name_elem = s.find("name")
            course_elem = s.find("course")
            sem_elem = s.find("semester")

            name = name_elem.text if name_elem is not None and name_elem.text else "N/A"
            course = course_elem.text if course_elem is not None and course_elem.text else "N/A"
            sem = sem_elem.text if sem_elem is not None and sem_elem.text else "N/A"

            print("Student found:")
            print(f"ID: {student_id}")
            print(f"Name: {name}")
            print(f"Course: {course}")
            print(f"Semester: {sem}")
            return

    print("Student not found.")


def update_student():
    """
    Locate an existing student and allow the user to change the name, course,
    or semester. Pressing Enter keeps the current value.
    """
    tree, root = load_tree()
    student_id = input("Enter student ID to update: ").strip()

    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    target = None
    for s in root.findall("student"):
        if s.attrib.get("id", "").strip() == student_id:
            target = s
            break

    if target is None:
        print("Student not found.")
        return

    name_elem = target.find("name")
    course_elem = target.find("course")
    sem_elem = target.find("semester")

    curr_name = name_elem.text if name_elem is not None and name_elem.text else ""
    curr_course = course_elem.text if course_elem is not None and course_elem.text else ""
    curr_sem = sem_elem.text if sem_elem is not None and sem_elem.text else ""

    print("Press Enter to keep the current value.")
    new_name = input(f"Name [{curr_name}]: ").strip()
    new_course = input(f"Course [{curr_course}]: ").strip()
    new_sem = input(f"Semester [{curr_sem}]: ").strip()

    if new_name:
        if name_elem is None:
            name_elem = ET.SubElement(target, "name")
        name_elem.text = new_name

    if new_course:
        if course_elem is None:
            course_elem = ET.SubElement(target, "course")
        course_elem.text = new_course

    if new_sem:
        if sem_elem is None:
            sem_elem = ET.SubElement(target, "semester")
        sem_elem.text = new_sem

    save_tree(tree)
    print("Student record updated successfully.")


def delete_student():
    """
    Locate the selected student and remove the student element from the root.
    Then save the updated XML document.
    """
    tree, root = load_tree()
    student_id = input("Enter student ID to delete: ").strip()

    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    target = None
    for s in root.findall("student"):
        if s.attrib.get("id", "").strip() == student_id:
            target = s
            break

    if target is None:
        print("Student not found.")
        return

    # Confirmation
    confirm = input(f"Are you sure you want to delete student with ID '{student_id}'? (y/n): ").strip().lower()
    if confirm in ["y", "yes"]:
        root.remove(target)
        save_tree(tree)
        print("Student record deleted successfully.")
    else:
        print("Deletion cancelled.")


def main():
    """
    Main application loop presenting the interactive menu.
    """
    # Ensure XML file is loaded / created on startup
    load_tree()

    while True:
        print("\n===== STUDENT RECORD MANAGEMENT USING XML =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Exiting application. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice! Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
