import os
from db_manager import Database

# Make sure the folder exists
DATABASE_FOLDER = "database_files"
os.makedirs(DATABASE_FOLDER, exist_ok=True)   # Create folder if not exist
DATABASE_FILE = os.path.join(DATABASE_FOLDER, "Checkinout.pkl")

def main():
    # Always start fresh for manual testing
    if os.path.exists(DATABASE_FILE):
        print("LOADING EXISTING DATABASE...")
        db = Database.load_database(DATABASE_FILE)

    else:
        print("CREATING NEW DATABASE...")
        db = Database("Testing.pkl")
        # Save database
        db.save_database(DATABASE_FILE)
        print("Database saved.")



    # row = ["roll_no", "name", "department","gender","email","hostel_name","room_no"]
    # # Create a simple table
    # db.create_table(
    #     name="student",
    #     columns=row,
    #     primary_key="roll_no",
    #     index_type="bplustree"
    # )
    # print("Table created.")
    # db.save_database(DATABASE_FILE)

    print(db.tables['students'].rows['1'])

    # # Insert some records
    # db.insert("students", {"roll_no": 24210118, "name": "Singh Prakash", "department": "ME", "gender" : "Male", "email" : "prakash@gmail.com", "hostel_name" : "Duven", "room_no" : "D416"})
    # db.insert("students", {"roll_no": 24210119, "name": "Aniket Asati", "department": "CIVIL", "gender" : "Male", "email" : "aniket@gmail.com", "hostel_name" : "Kyzeel", "room_no" : "K205"})
    # db.insert("students", {"roll_no": 24210120, "name": "vipul Chauhan", "department": "EE", "gender" : "Male", "email" : "vipul@gmail.com", "hostel_name" : "Firpeal", "room_no" : "F125"})
    # print("Records inserted.")
    # db.save_database(DATABASE_FILE)
    # print("Data saved...")

    # # Update a record
    # db.update("students", 24210118, {"email": "singh@gmail.com"})
    # print("Record updated.")
    # db.save_database(DATABASE_FILE)

    # # Search for a record
    # record = db.search("students", 24210118)
    # print(f"Record with ID 24210115: {record}")

    # # Print all records of a table
    # db.print_records("students")

    # # Delete a record
    # db.delete("students", 24210118)
    # print("Record with ID 24210118 deleted.")
    # db.save_database(DATABASE_FILE)
    # print("record deleted...")

    # # Perform a range query
    # results = db.range_query("students", 24210115, 24210118)
    # print(f"Range query results: {results}")


if __name__ == "__main__":
    main()
