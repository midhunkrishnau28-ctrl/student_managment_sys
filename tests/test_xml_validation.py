"""
================================================================================
Test Suite for XML Validation against XSD Schema
Tests that students.xml validates against students.xsd using lxml.
================================================================================
"""

import os
import sys
import unittest
import xml.etree.ElementTree as ET

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from modules.xml_handler import validate_with_xsd, load_tree, save_tree

TEST_XML = os.path.join(PROJECT_ROOT, "tests", "test_xsd_students.xml")
XSD_FILE = os.path.join(PROJECT_ROOT, "students.xsd")


class TestXMLValidation(unittest.TestCase):
    """Test cases for XSD schema validation."""

    def setUp(self):
        """Create a valid test XML file."""
        root = ET.Element("students")
        s1 = ET.SubElement(root, "student", attrib={"id": "101"})
        ET.SubElement(s1, "name").text = "Anu"
        ET.SubElement(s1, "course").text = "M.Tech CSE"
        ET.SubElement(s1, "semester").text = "1"
        tree = ET.ElementTree(root)
        try:
            ET.indent(tree, space="    ", level=0)
        except AttributeError:
            pass
        tree.write(TEST_XML, encoding="UTF-8", xml_declaration=True)

    def tearDown(self):
        if os.path.exists(TEST_XML):
            os.remove(TEST_XML)

    def test_valid_xml_passes_xsd(self):
        """TC-XSD-01: Valid XML should pass XSD validation."""
        is_valid, msg = validate_with_xsd(TEST_XML, XSD_FILE)
        # May fail if lxml is not installed - still a valid test outcome
        if "lxml" in msg:
            self.skipTest("lxml not installed – skipping XSD validation test.")
        self.assertTrue(is_valid, msg)

    def test_invalid_xml_fails_xsd(self):
        """TC-XSD-02: XML missing required elements should fail validation."""
        # Create XML with missing 'name' element
        root = ET.Element("students")
        s1 = ET.SubElement(root, "student", attrib={"id": "201"})
        # Intentionally missing <name>
        ET.SubElement(s1, "course").text = "B.Tech"
        ET.SubElement(s1, "semester").text = "2"
        tree = ET.ElementTree(root)
        tree.write(TEST_XML, encoding="UTF-8", xml_declaration=True)

        is_valid, msg = validate_with_xsd(TEST_XML, XSD_FILE)
        if "lxml" in msg:
            self.skipTest("lxml not installed – skipping XSD validation test.")
        self.assertFalse(is_valid)

    def test_missing_xsd_file(self):
        """TC-XSD-03: Missing XSD file should return failure."""
        is_valid, msg = validate_with_xsd(TEST_XML, "nonexistent.xsd")
        self.assertFalse(is_valid)
        self.assertIn("not found", msg)

    def test_missing_xml_file(self):
        """TC-XSD-04: Missing XML file should return failure."""
        is_valid, msg = validate_with_xsd("nonexistent.xml", XSD_FILE)
        self.assertFalse(is_valid)
        self.assertIn("not found", msg)

    def test_empty_xml_passes_xsd(self):
        """TC-XSD-05: An empty <students/> document should validate."""
        root = ET.Element("students")
        tree = ET.ElementTree(root)
        tree.write(TEST_XML, encoding="UTF-8", xml_declaration=True)

        is_valid, msg = validate_with_xsd(TEST_XML, XSD_FILE)
        if "lxml" in msg:
            self.skipTest("lxml not installed – skipping XSD validation test.")
        self.assertTrue(is_valid, msg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
