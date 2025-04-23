# Database_bplustree# CheckInOut Database Management System

## Project Overview

Welcome to the **CheckInOut** Database Management System! This project provides a lightweight, file-based database management system featuring:

- Database creation and persistence.
- Table creation and deletion.
- Insert, update, delete, search, and range queries.
- Dashboard interface to manage operations.
- Performance comparison between naive list-based storage and a B+ Tree index.

---

## 📂 File Hierarchy

```
Module 4/
|
|-- database/
|   |-- templates/
|   |   |-- update_record.html
|
|-- Tests/
|   |-- __pycache__/
|   |-- performance_test.py
|   |-- performance_test-1.py
|   |-- test_bplustree.py
|   |-- __init__.py
|   |-- manual_test.py
|
|-- app.py
|-- bplustree.py
|-- bruteforce.py
|-- db_manager.py
|-- performance.py
|-- tables.py
|-- performance_plots/
|   |-- students_search_times.png
|-- README.md
|-- report.ipynb
|-- requirements.txt
```

---

## ✨ Features

- **Dashboard Interface:**
  - **Create Database:** Create a new database from scratch.
  - **Use Existing Database:** View and operate on existing databases.

- **Pre-loaded Database:**
  - **Database:** `checkinout`
  - **Tables:** `students`, `staff`

- **Operations Supported:**
  - Create and delete databases.
  - Create and delete tables.
  - Insert new records.
  - Update existing records.
  - Delete records.
  - Search records.
  - Perform range queries.
  - Display all records.

- **Persistence:**
  - All databases and tables are **saved** and can be **loaded** even after restarting the application.

- **Performance Analysis Section:**
  - Compare B+ Tree indexing vs naive list-based search.
  - Graphical analysis for:
    - Insertion
    - Searching
    - Deletion
    - Range Query

---

## 🚀 Beginner Tutorial to Run the App

1. **Clone the Repository:**

```bash
https://https://github.com/WasimKaunain/Database_bplustree
```

2. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the App:**

```bash
python app.py
```

4. **Access the Dashboard:**

Open your browser and go to:

```
http://127.0.0.1:5000/
```

5. **Using the Dashboard:**
   - Choose "Create Database" to create a new one.
   - Choose "Use Existing Database" to select from pre-existing databases (like `checkinout`).
   - Perform operations like insert, update, delete, search, range queries, and view records easily.

6. **Performance Testing:**
   - Go to the **Performance Analysis** section.
   - Compare search, insert, delete, and range query times between **Naive List** vs **B+ Tree** using graphs.

---

## 📊 Technologies Used

- **Python**
- **Flask** (for dashboard web interface)
- **HTML/CSS** (for simple frontend forms)
- **Matplotlib** (for performance plotting)
- **Custom Database Management System** (developed from scratch)
- **B+ Tree Data Structure** (for indexing and fast searching)

---

## 💡 Final Notes

This project aims to mimic real-world database operations with a minimalistic and understandable design. It is ideal for beginners who want to:
- Learn how database management systems work internally.
- Understand indexing concepts through practical examples.
- See the impact of data structures on performance.

