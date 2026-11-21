"""
================================================================================
Test Suite for Student Operations
Tests all CRUD operations on students.xml using Python's unittest framework.
================================================================================
"""

import os
import sys
import unittest
import xml.etree.ElementTree as ET

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from modules.student_operations import (
    get_all_students,
    find_student_by_id,
    add_student,
    update_student,
    delete_student,
    get_summary_stats,
)
from modules.xml_handler import load_tree, save_tree

# Use a dedicated test XML file so we don't modify the real data
TEST_XML = os.path.join(PROJECT_ROOT, "tests", "test_students.xml")


class TestStudentOperations(unittest.TestCase):
    """Test cases for CRUD operations on student records."""

    def setUp(self):
        """Create a fresh test XML file before each test."""
        root = ET.Element("students")
        # Seed with two sample records
        s1 = ET.SubElement(root, "student", attrib={"id": "101"})
        ET.SubElement(s1, "name").text = "Anu"
        ET.SubElement(s1, "course").text = "M.Tech CSE"
        ET.SubElement(s1, "semester").text = "1"

        s2 = ET.SubElement(root, "student", attrib={"id": "102"})
        ET.SubElement(s2, "name").text = "Rahul"
        ET.SubElement(s2, "course").text = "M.Tech CSE"
        ET.SubElement(s2, "semester").text = "1"

        tree = ET.ElementTree(root)
        try:
            ET.indent(tree, space="    ", level=0)
        except AttributeError:
            pass
        tree.write(TEST_XML, encoding="UTF-8", xml_declaration=True)

    def tearDown(self):
        """Remove the test XML file after each test."""
        if os.path.exists(TEST_XML):
            os.remove(TEST_XML)

    # ---- TC-01: Add new student ----
    def test_add_student_success(self):
        """TC-01: Adding a new student with valid data should succeed."""
        success, msg = add_student("103", "Sneha", "M.Tech CSE", "2", TEST_XML)
        self.assertTrue(success)
        self.assertIn("103", msg)
        student = find_student_by_id("103", TEST_XML)
        self.assertIsNotNone(student)
        self.assertEqual(student["name"], "Sneha")

    # ---- TC-02: Add student with duplicate ID ----
    def test_add_duplicate_id(self):
        """TC-02: Adding a student with an existing ID should fail."""
        success, msg = add_student("101", "Duplicate", "B.Tech", "3", TEST_XML)
        self.assertFalse(success)
        self.assertIn("already exists", msg)

    # ---- TC-03: Add student with empty fields ----
    def test_add_empty_id(self):
        """TC-03: Adding a student with empty ID should fail."""
        success, msg = add_student("", "Name", "Course", "1", TEST_XML)
        self.assertFalse(success)

    def test_add_empty_name(self):
        """TC-03b: Adding a student with empty name should fail."""
        success, msg = add_student("200", "", "Course", "1", TEST_XML)
        self.assertFalse(success)

    def test_add_empty_course(self):
        """TC-03c: Adding a student with empty course should fail."""
        success, msg = add_student("200", "Name", "", "1", TEST_XML)
        self.assertFalse(success)

    def test_add_empty_semester(self):
        """TC-03d: Adding a student with empty semester should fail."""
        success, msg = add_student("200", "Name", "Course", "", TEST_XML)
        self.assertFalse(success)

    # ---- TC-04: View all students ----
    def test_view_all_students(self):
        """TC-04: Should return all seeded student records."""
        students = get_all_students(TEST_XML)
        self.assertEqual(len(students), 2)
        ids = [s["id"] for s in students]
        self.assertIn("101", ids)
        self.assertIn("102", ids)

    # ---- TC-05: View students when empty ----
    def test_view_empty(self):
        """TC-05: Should return an empty list when no records exist."""
        # Create empty XML
        root = ET.Element("students")
        tree = ET.ElementTree(root)
        tree.write(TEST_XML, encoding="UTF-8", xml_declaration=True)

        students = get_all_students(TEST_XML)
        self.assertEqual(len(students), 0)

    # ---- TC-06: Search existing student ----
    def test_search_existing(self):
        """TC-06: Searching for an existing student should return their data."""
        student = find_student_by_id("101", TEST_XML)
        self.assertIsNotNone(student)
        self.assertEqual(student["name"], "Anu")
        self.assertEqual(student["course"], "M.Tech CSE")

    # ---- TC-07: Search nonexistent student ----
    def test_search_nonexistent(self):
        """TC-07: Searching for a nonexistent ID should return None."""
        student = find_student_by_id("999", TEST_XML)
        self.assertIsNone(student)

    # ---- TC-08: Update student information ----
    def test_update_student(self):
        """TC-08: Updating a student's name should persist the change."""
        success, msg, updated = update_student("101", name="Anu Sharma", xml_file=TEST_XML)
        self.assertTrue(success)
        self.assertEqual(updated["name"], "Anu Sharma")
        # Verify persistence
        student = find_student_by_id("101", TEST_XML)
        self.assertEqual(student["name"], "Anu Sharma")

    # ---- TC-09: Update selected fields only ----
    def test_update_partial(self):
        """TC-09: Updating only semester should keep other fields unchanged."""
        success, msg, updated = update_student("101", semester="3", xml_file=TEST_XML)
        self.assertTrue(success)
        self.assertEqual(updated["semester"], "3")
        self.assertEqual(updated["name"], "Anu")  # unchanged
        self.assertEqual(updated["course"], "M.Tech CSE")  # unchanged

    # ---- TC-10: Update nonexistent student ----
    def test_update_nonexistent(self):
        """TC-10: Updating a nonexistent student should fail."""
        success, msg, updated = update_student("999", name="Ghost", xml_file=TEST_XML)
        self.assertFalse(success)
        self.assertIsNone(updated)

    # ---- TC-11: Delete existing student ----
    def test_delete_student(self):
        """TC-11: Deleting an existing student should remove their record."""
        success, msg = delete_student("101", TEST_XML)
        self.assertTrue(success)
        self.assertIsNone(find_student_by_id("101", TEST_XML))
        self.assertEqual(len(get_all_students(TEST_XML)), 1)

    # ---- TC-12: Delete nonexistent student ----
    def test_delete_nonexistent(self):
        """TC-12: Deleting a nonexistent student should fail."""
        success, msg = delete_student("999", TEST_XML)
        self.assertFalse(success)
        self.assertIn("not found", msg)

    # ---- TC-13: Data persistence across reload ----
    def test_data_persistence(self):
        """TC-13: Data should persist after adding and re-loading."""
        add_student("105", "Persistent", "MBA", "2", TEST_XML)
        # Reload from file
        students = get_all_students(TEST_XML)
        ids = [s["id"] for s in students]
        self.assertIn("105", ids)

    # ---- TC-14: Summary statistics ----
    def test_summary_stats(self):
        """TC-14: Summary should report correct counts."""
        stats = get_summary_stats(TEST_XML)
        self.assertEqual(stats["total_students"], 2)
        self.assertGreaterEqual(stats["total_courses"], 1)
        self.assertGreaterEqual(stats["total_semesters"], 1)

    # ---- TC-15: Handle missing XML file ----
    def test_missing_xml_auto_create(self):
        """TC-15: load_tree should create the file if it doesn't exist."""
        missing = os.path.join(PROJECT_ROOT, "tests", "missing.xml")
        if os.path.exists(missing):
            os.remove(missing)
        tree, root = load_tree(missing)
        self.assertTrue(os.path.exists(missing))
        self.assertEqual(root.tag, "students")
        os.remove(missing)


if __name__ == "__main__":
    unittest.main(verbosity=2)
