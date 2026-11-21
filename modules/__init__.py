"""
Student Record Management System Modules Package
"""

from .xml_handler import load_tree, save_tree, get_xml_content, validate_with_xsd
from .student_operations import (
    get_all_students,
    find_student_by_id,
    add_student,
    update_student,
    delete_student,
    get_summary_stats
)
from .validation import validate_student_id, validate_student_fields, sanitize_input

__all__ = [
    "load_tree",
    "save_tree",
    "get_xml_content",
    "validate_with_xsd",
    "get_all_students",
    "find_student_by_id",
    "add_student",
    "update_student",
    "delete_student",
    "get_summary_stats",
    "validate_student_id",
    "validate_student_fields",
    "sanitize_input"
]
