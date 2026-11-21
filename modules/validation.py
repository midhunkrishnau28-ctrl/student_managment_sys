"""
Student Record Management System - Input Validation Module
Provides validation functions for student details before writing to XML.
"""

from typing import Tuple, Optional, Dict, Any


def validate_student_id(student_id: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that student ID is non-empty and contains valid characters.
    """
    if student_id is None:
        return False, "Student ID cannot be null."
    
    clean_id = str(student_id).strip()
    if not clean_id:
        return False, "Student ID cannot be empty."
    
    if len(clean_id) > 50:
        return False, "Student ID exceeds maximum length of 50 characters."
        
    return True, None


def validate_student_fields(name: str, course: str, semester: str) -> Tuple[bool, Optional[str]]:
    """
    Validate name, course, and semester fields.
    """
    if name is None or not str(name).strip():
        return False, "Student name cannot be empty."
    
    if course is None or not str(course).strip():
        return False, "Course name cannot be empty."
        
    if semester is None or not str(semester).strip():
        return False, "Semester cannot be empty."
        
    clean_sem = str(semester).strip()
    # If semester is a digit, verify reasonable range (1-12)
    if clean_sem.isdigit():
        sem_num = int(clean_sem)
        if sem_num < 1 or sem_num > 12:
            return False, "Semester number must be between 1 and 12."
            
    return True, None


def sanitize_input(value: Any) -> str:
    """
    Sanitize string input by stripping whitespace.
    """
    if value is None:
        return ""
    return str(value).strip()
