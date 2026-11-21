# Student Record Management System Using XML

## M.Tech Computer Science and Engineering Academic Project

**Royal College of Engineering & Technology, Akkikavu**
**APJ Abdul Kalam Technological University**

**Student:** SNEHA V P (RCE26CS058)
**Guide:** SARIGA S, Assistant Professor, CSE Department

---

## 1. Project Introduction

This application demonstrates the practical use of **XML (Extensible Markup Language)** for structured student information storage and management. It allows users to efficiently **Add, View, Search, Update, and Delete** student records stored in an XML file (`students.xml`).

The system uses Python's built-in `xml.etree.ElementTree` library to create, read, parse, modify, and manipulate XML documents. An XML Schema Definition (`students.xsd`) describes the expected XML structure and can be used for validation.

---

## 2. Project Objectives

- Develop a system to manage student records using Python and XML
- Demonstrate XML as a structured data storage mechanism
- Use ElementTree for all XML processing operations
- Provide both a **command-line interface** (`main.py`) and a **modern web interface** (`app.py`)
- Include XSD-based validation of the XML document
- Implement full CRUD operations with input validation and error handling

---

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.x** | Programming language |
| **XML** | Data storage (`students.xml`) |
| **xml.etree.ElementTree** | XML processing (built-in) |
| **XSD** | XML Schema Definition (`students.xsd`) |
| **Flask** | Web framework for the browser-based interface |
| **lxml** | Optional library for XSD schema validation |
| **HTML / CSS / JavaScript** | Frontend (web interface) |
| **Bootstrap 5** | UI styling framework |

---

## 4. System Requirements

- **Python 3.9+** (Python 3.x required; 3.9+ recommended for `ET.indent()`)
- **Flask** (for the web interface)
- **lxml** (optional, for XSD validation)
- **Web browser** (for the web interface)
- **Operating System:** Windows / Linux / macOS

---

## 5. Project Folder Structure

```
Student_Record_Management_System/
│
├── main.py                       # Menu-driven CLI application
├── app.py                        # Flask web application
│
├── students.xml                  # XML data file (auto-created if missing)
├── students.xsd                  # XML Schema Definition
│
├── requirements.txt              # Python dependencies
├── README.md                     # This documentation
│
├── modules/                      # Backend Python modules
│   ├── __init__.py
│   ├── xml_handler.py            # XML load, save, validate operations
│   ├── student_operations.py     # CRUD operations on student records
│   └── validation.py             # Input validation utilities
│
├── templates/                    # Jinja2 HTML templates (Flask)
│   ├── base.html                 # Base layout with sidebar navigation
│   ├── dashboard.html            # Dashboard with statistics
│   ├── add_student.html          # Add student form
│   ├── view_students.html        # View all students table
│   ├── search_student.html       # Search by student ID
│   ├── update_student.html       # Update student details
│   ├── delete_student.html       # Delete with confirmation
│
├── static/                       # Static assets
│   ├── css/
│   │   └── style.css             # Custom CSS stylesheet
│   └── js/
│       └── script.js             # Custom JavaScript
│
└── tests/                        # Test suite
    ├── test_student_operations.py # CRUD operation tests
    └── test_xml_validation.py     # XSD validation tests
```

---

## 6. Installation Instructions

### Step 1: Navigate to the project folder

```bash
cd "XML PROJECT"
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Flask** – lightweight web framework
- **lxml** – XML schema validation library (optional)

---

## 7. How to Run the Application

### Option A: Web Interface (Recommended)

```bash
python app.py
```

Open your browser and go to: **http://127.0.0.1:5000**

### Option B: Command-Line Interface

```bash
python main.py
```

This presents an interactive text menu:

```
===== STUDENT RECORD MANAGEMENT USING XML =====
1. Add Student
2. View Students
3. Search Student
4. Update Student
5. Delete Student
6. Exit
Enter your choice (1-6):
```

---

## 8. How to Add a Student

### Web Interface
1. Click **"Add Student"** in the sidebar
2. Fill in: Student ID, Name, Course, Semester
3. Click **"Add Student"** button
4. A success message appears and you are redirected to the student list

### CLI
1. Choose option **1** from the menu
2. Enter each field when prompted
3. The system confirms the addition

---

## 9. How to View Student Records

### Web Interface
- Click **"View Students"** in the sidebar
- All records are displayed in a formatted table with Edit/Delete buttons

### CLI
- Choose option **2** from the menu
- Records are printed in a formatted list

---

## 10. How to Search Student Records

### Web Interface
1. Click **"Search Student"** in the sidebar
2. Enter the Student ID in the search box
3. Click **"Search"**
4. The matching record is displayed, or a "Not Found" message appears

### CLI
- Choose option **3** and enter the Student ID

---

## 11. How to Update Student Records

### Web Interface
1. Click **"Update Student"** in the sidebar
2. Enter the Student ID and click **"Find Student"**
3. The form is pre-filled with current values
4. Modify the desired fields (leave empty to keep current value)
5. Click **"Update Student"**

### CLI
- Choose option **4**, enter the Student ID, then modify fields (press Enter to keep current)

---

## 12. How to Delete Student Records

### Web Interface
1. Click **"Delete Student"** in the sidebar
2. Enter the Student ID and click **"Find Student"**
3. The student's details are shown with a confirmation prompt
4. Click **"Yes, Delete This Student"** to confirm

### CLI
- Choose option **5**, enter the Student ID, confirm with `y`

---

## 13. XML Document Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<students>
    <student id="101">
        <name>Anu</name>
        <course>M.Tech CSE</course>
        <semester>1</semester>
    </student>
    <student id="102">
        <name>Rahul</name>
        <course>M.Tech CSE</course>
        <semester>1</semester>
    </student>
</students>
```

- `<students>` – root element
- `<student>` – one per record; `id` attribute stores the Student ID
- `<name>`, `<course>`, `<semester>` – child elements

---

## 14. XSD Schema Explanation

The `students.xsd` file defines:

| Aspect | Definition |
|---|---|
| Root element | `<students>` |
| Child elements | Zero or more `<student>` elements |
| Student children | `<name>`, `<course>`, `<semester>` (in order) |
| Student ID | Required attribute (`id`) of type `NonEmptyString` |
| Uniqueness | `<xs:unique>` constraint ensures no duplicate IDs |
| Semester | String type, length 1–10 |

---

## 15. Testing Instructions

Run all tests from the project root:

```bash
python -m pytest tests/ -v
```

Or using unittest:

```bash
python -m unittest discover -s tests -v
```

### Test Coverage

| Test ID | Description |
|---|---|
| TC-01 | Add a new student with valid data |
| TC-02 | Add a student with duplicate ID |
| TC-03 | Add student with empty fields |
| TC-04 | View all student records |
| TC-05 | View records when database is empty |
| TC-06 | Search for existing student |
| TC-07 | Search for nonexistent student |
| TC-08 | Update student information |
| TC-09 | Update only selected fields |
| TC-10 | Update nonexistent student |
| TC-11 | Delete existing student |
| TC-12 | Delete nonexistent student |
| TC-13 | Data persistence after reload |
| TC-14 | Summary statistics |
| TC-15 | Auto-create missing XML file |
| TC-XSD-01 | Valid XML passes XSD |
| TC-XSD-02 | Invalid XML fails XSD |
| TC-XSD-03 | Missing XSD file handled |
| TC-XSD-04 | Missing XML file handled |
| TC-XSD-05 | Empty students document validates |

---

## 16. Expected Outputs

- **Dashboard:** Shows total students, courses, semesters, and distribution tables
- **Add Student:** Success/error messages with redirect
- **View Students:** Formatted table with all records
- **Search:** Detailed student card or "Not Found" message
- **Update:** Pre-filled form, success confirmation
- **Delete:** Confirmation prompt, success message

---

## License

This project is developed for academic purposes as part of the M.Tech CSE programme at Royal College of Engineering & Technology, Akkikavu, affiliated to APJ Abdul Kalam Technological University.
