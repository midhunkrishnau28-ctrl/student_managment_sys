"""
Student Record Management System - XML Handler Module
Uses Python's standard xml.etree.ElementTree library to manage XML documents.
Also includes optional XSD schema validation via lxml.
"""

import os
import xml.etree.ElementTree as ET
from typing import Tuple, Optional

# Default paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_XML_FILE = os.path.join(BASE_DIR, "students.xml")
DEFAULT_XSD_FILE = os.path.join(BASE_DIR, "students.xsd")


def load_tree(xml_file: str = DEFAULT_XML_FILE) -> Tuple[ET.ElementTree, ET.Element]:
    """
    Check whether the XML file exists. If not, create a new XML document with
    the root element <students>. Load and parse the XML document and return
    the XML tree and its root element.
    """
    if not os.path.exists(xml_file):
        # Create empty root element
        root = ET.Element("students")
        tree = ET.ElementTree(root)
        save_tree(tree, xml_file)
        return tree, root

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        if root.tag != "students":
            raise ValueError(f"Invalid root element: '<{root.tag}>'. Expected '<students>'.")
        return tree, root
    except (ET.ParseError, ValueError) as err:
        # Corrupted or malformed file: backup corrupted file and create a fresh one
        backup_file = f"{xml_file}.corrupted.bak"
        try:
            if os.path.exists(xml_file):
                os.replace(xml_file, backup_file)
        except OSError:
            pass

        root = ET.Element("students")
        tree = ET.ElementTree(root)
        save_tree(tree, xml_file)
        return tree, root


def save_tree(tree: ET.ElementTree, xml_file: str = DEFAULT_XML_FILE) -> None:
    """
    Write the XML tree to the given file path using UTF-8 encoding
    and standard XML declaration. Indent for readability.
    """
    root = tree.getroot()
    # Format tree with indentation for clean human-readable output
    try:
        ET.indent(tree, space="    ", level=0)
    except AttributeError:
        # Fallback for Python versions earlier than 3.9
        pass

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(os.path.abspath(xml_file)), exist_ok=True)
    tree.write(xml_file, encoding="UTF-8", xml_declaration=True)


def get_xml_content(xml_file: str = DEFAULT_XML_FILE) -> str:
    """
    Retrieve the raw text content of the XML file.
    """
    if not os.path.exists(xml_file):
        load_tree(xml_file)
        
    with open(xml_file, "r", encoding="utf-8") as f:
        return f.read()


def validate_with_xsd(xml_file: str = DEFAULT_XML_FILE, xsd_file: str = DEFAULT_XSD_FILE) -> Tuple[bool, str]:
    """
    Validate the XML document against the XSD schema definition.
    Uses lxml if installed, otherwise reports that lxml is needed.
    """
    if not os.path.exists(xml_file):
        return False, f"XML file not found at: {xml_file}"
        
    if not os.path.exists(xsd_file):
        return False, f"XSD schema file not found at: {xsd_file}"

    try:
        from lxml import etree
        with open(xsd_file, "rb") as schema_file:
            schema_root = etree.XML(schema_file.read())
            schema = etree.XMLSchema(schema_root)

        with open(xml_file, "rb") as doc_file:
            doc = etree.parse(doc_file)

        schema.assertValid(doc)
        return True, "XML document successfully validated against students.xsd schema."
    except ImportError:
        return False, "lxml library is not installed for XSD validation. Run: pip install lxml"
    except Exception as e:
        return False, f"XML Schema Validation Error: {str(e)}"
