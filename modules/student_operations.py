"""
Student Record Management System - Student Operations Module
Implements CRUD (Create, Read, Update, Delete) and search operations
on student records stored in students.xml using xml.etree.ElementTree.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Tuple, Any
from .xml_handler import load_tree, save_tree, DEFAULT_XML_FILE
from .validation import validate_student_id, validate_student_fields, sanitize_input


def get_all_students(xml_file: str = DEFAULT_XML_FILE) -> List[Dict[str, str]]:
    """
    Retrieve all student records from the XML document.
    Returns a list of dictionaries with keys: id, name, course, semester.
    """
    tree, root = load_tree(xml_file)
    students = []
    
    for student_elem in root.findall("student"):
        s_id = student_elem.attrib.get("id", "").strip()
        name_elem = student_elem.find("name")
        course_elem = student_elem.find("course")
        sem_elem = student_elem.find("semester")
        
        students.append({
            "id": s_id,
            "name": name_elem.text.strip() if name_elem is not None and name_elem.text else "",
            "course": course_elem.text.strip() if course_elem is not None and course_elem.text else "",
            "semester": sem_elem.text.strip() if sem_elem is not None and sem_elem.text else ""
        })
        
    return students


def find_student_by_id(student_id: str, xml_file: str = DEFAULT_XML_FILE) -> Optional[Dict[str, str]]:
    """
    Search for a student by student ID.
    Returns the student dictionary if found, or None if not found.
    """
    valid, err = validate_student_id(student_id)
    if not valid:
        return None
        
    clean_id = sanitize_input(student_id)
    tree, root = load_tree(xml_file)
    
    for student_elem in root.findall("student"):
        if student_elem.attrib.get("id", "").strip() == clean_id:
            name_elem = student_elem.find("name")
            course_elem = student_elem.find("course")
            sem_elem = student_elem.find("semester")
            return {
                "id": clean_id,
                "name": name_elem.text.strip() if name_elem is not None and name_elem.text else "",
                "course": course_elem.text.strip() if course_elem is not None and course_elem.text else "",
                "semester": sem_elem.text.strip() if sem_elem is not None and sem_elem.text else ""
            }
            
    return None


def add_student(student_id: str, name: str, course: str, semester: str, xml_file: str = DEFAULT_XML_FILE) -> Tuple[bool, str]:
    """
    Add a new student record to the XML document.
    Checks for empty values and duplicate student IDs.
    """
    # Validate ID
    valid_id, err_id = validate_student_id(student_id)
    if not valid_id:
        return False, err_id or "Invalid student ID."
        
    # Validate fields
    valid_fields, err_fields = validate_student_fields(name, course, semester)
    if not valid_fields:
        return False, err_fields or "Invalid student details."
        
    clean_id = sanitize_input(student_id)
    clean_name = sanitize_input(name)
    clean_course = sanitize_input(course)
    clean_semester = sanitize_input(semester)
    
    tree, root = load_tree(xml_file)
    
    # Check for duplicate student ID
    for student_elem in root.findall("student"):
        if student_elem.attrib.get("id", "").strip() == clean_id:
            return False, f"Duplicate Error: Student ID '{clean_id}' already exists."
            
    # Create new student element and child elements
    new_student = ET.Element("student", attrib={"id": clean_id})
    
    elem_name = ET.SubElement(new_student, "name")
    elem_name.text = clean_name
    
    elem_course = ET.SubElement(new_student, "course")
    elem_course.text = clean_course
    
    elem_semester = ET.SubElement(new_student, "semester")
    elem_semester.text = clean_semester
    
    # Append to root and save
    root.append(new_student)
    save_tree(tree, xml_file)
    
    return True, f"Student with ID '{clean_id}' added successfully."


def update_student(
    student_id: str,
    name: Optional[str] = None,
    course: Optional[str] = None,
    semester: Optional[str] = None,
    xml_file: str = DEFAULT_XML_FILE
) -> Tuple[bool, str, Optional[Dict[str, str]]]:
    """
    Update an existing student's details. If any field is left empty or None,
    the existing value is retained.
    """
    valid_id, err_id = validate_student_id(student_id)
    if not valid_id:
        return False, err_id or "Invalid student ID.", None
        
    clean_id = sanitize_input(student_id)
    tree, root = load_tree(xml_file)
    target_elem = None
    
    for student_elem in root.findall("student"):
        if student_elem.attrib.get("id", "").strip() == clean_id:
            target_elem = student_elem
            break
            
    if target_elem is None:
        return False, f"Update Error: Student with ID '{clean_id}' not found.", None
        
    # Name
    name_elem = target_elem.find("name")
    if name is not None and str(name).strip():
        if name_elem is None:
            name_elem = ET.SubElement(target_elem, "name")
        name_elem.text = sanitize_input(name)
        
    # Course
    course_elem = target_elem.find("course")
    if course is not None and str(course).strip():
        if course_elem is None:
            course_elem = ET.SubElement(target_elem, "course")
        course_elem.text = sanitize_input(course)
        
    # Semester
    sem_elem = target_elem.find("semester")
    if semester is not None and str(semester).strip():
        if sem_elem is None:
            sem_elem = ET.SubElement(target_elem, "semester")
        sem_elem.text = sanitize_input(semester)
        
    save_tree(tree, xml_file)
    
    updated_data = {
        "id": clean_id,
        "name": name_elem.text if name_elem is not None and name_elem.text else "",
        "course": course_elem.text if course_elem is not None and course_elem.text else "",
        "semester": sem_elem.text if sem_elem is not None and sem_elem.text else ""
    }
    
    return True, f"Student record for ID '{clean_id}' updated successfully.", updated_data


def delete_student(student_id: str, xml_file: str = DEFAULT_XML_FILE) -> Tuple[bool, str]:
    """
    Delete a student record from the XML document by Student ID.
    """
    valid_id, err_id = validate_student_id(student_id)
    if not valid_id:
        return False, err_id or "Invalid student ID."
        
    clean_id = sanitize_input(student_id)
    tree, root = load_tree(xml_file)
    target_elem = None
    
    for student_elem in root.findall("student"):
        if student_elem.attrib.get("id", "").strip() == clean_id:
            target_elem = student_elem
            break
            
    if target_elem is None:
        return False, f"Delete Error: Student with ID '{clean_id}' not found."
        
    root.remove(target_elem)
    save_tree(tree, xml_file)
    
    return True, f"Student with ID '{clean_id}' deleted successfully."


def get_summary_stats(xml_file: str = DEFAULT_XML_FILE) -> Dict[str, Any]:
    """
    Calculate summary metrics from the XML file:
    total students, unique courses, unique semesters, and course distribution.
    """
    students = get_all_students(xml_file)
    total_students = len(students)
    courses = set()
    semesters = set()
    course_counts: Dict[str, int] = {}
    semester_counts: Dict[str, int] = {}
    
    for s in students:
        c = s["course"] or "Unassigned"
        sem = s["semester"] or "Unassigned"
        courses.add(c)
        semesters.add(sem)
        course_counts[c] = course_counts.get(c, 0) + 1
        semester_counts[sem] = semester_counts.get(sem, 0) + 1
        
    return {
        "total_students": total_students,
        "total_courses": len(courses),
        "total_semesters": len(semesters),
        "courses_list": sorted(list(courses)),
        "semesters_list": sorted(list(semesters)),
        "course_distribution": course_counts,
        "semester_distribution": semester_counts
    }
