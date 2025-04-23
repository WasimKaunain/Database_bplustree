import os
import time
import random
import matplotlib.pyplot as plt
from db_manager import Database
from performance import PerformanceAnalyzer

def generate_test_sizes():
    return range(100, 10001, 1000)

def generate_staff_department():
    departments = ['CSE', 'EE', 'CE', 'ME', 'ICDT', 'SPML', 'AI']
    return random.choice(departments)

def create_rows(table_name, num_rows):
    rows = []
    if table_name == "students":
        for i in range(1, num_rows + 1):
            rows.append({
                "id": i,
                "name": f"Student_{i}",
                "email": f"Student_{i}@example.com"
            })
    elif table_name == "staff":
        for i in range(1, num_rows + 1):
            rows.append({
                "id": i,
                "name": f"Staff_{i}",
                "department": generate_staff_department()
            })
    return rows

def measure_insertion_performance(table_name,db_name):
    test_sizes = generate_test_sizes()
    bplus_times = []
    brute_times = []

    for num_rows in test_sizes:
        print(f"Insertion: {num_rows} rows for {table_name}")
        rows = create_rows(table_name, num_rows)

        # B+Tree
        db_bplus = Database(db_name)
        db_bplus.create_table(table_name, list(rows[0].keys()), primary_key="id", index_type="bplustree")
        insert_time = PerformanceAnalyzer.measure_insertion_time(db_bplus, table_name, rows)
        bplus_times.append(insert_time)

        # BruteForce
        db_brute = Database(db_name)
        db_brute.create_table(table_name, list(rows[0].keys()), primary_key="id", index_type="bruteforce")
        insert_time = PerformanceAnalyzer.measure_insertion_time(db_brute, table_name, rows)
        brute_times.append(insert_time)

    return test_sizes, bplus_times, brute_times

def measure_search_performance(table_name,db_name):
    test_sizes = generate_test_sizes()
    bplus_times = []
    brute_times = []

    for num_rows in test_sizes:
        print(f"Search: {num_rows} rows for {table_name}")
        rows = create_rows(table_name, num_rows)

        db_bplus = Database(db_name)
        db_bplus.create_table(table_name, list(rows[0].keys()), primary_key="id", index_type="bplustree")
        db_bplus.insert_bulk(table_name, rows)

        search_ids = [1, num_rows // 2, num_rows]
        search_time = PerformanceAnalyzer.measure_search_time(db_bplus, table_name, search_ids)
        bplus_times.append(search_time)

        db_brute = Database(db_name)
        db_brute.create_table(table_name, list(rows[0].keys()), primary_key="id", index_type="bruteforce")
        db_brute.insert_bulk(table_name, rows)

        search_time = PerformanceAnalyzer.measure_search_time(db_brute, table_name, search_ids)
        brute_times.append(search_time)

    return test_sizes, bplus_times, brute_times

def measure_range_query_performance(table_name,db_name):
    test_sizes = generate_test_sizes()
    bplus_times = []
    brute_times = []

    for num_rows in test_sizes:
        print(f"Range Query: {num_rows} rows for {table_name}")
        rows = create_rows(table_name, num_rows)

        db_bplus = Database(db_name)
        db_bplus.create_table(table_name, list(rows[0].keys()), primary_key="id", index_type="bplustree")
        db_bplus.insert_bulk(table_name, rows)

        ranges = [(1, num_rows // 2), (num_rows // 2, num_rows)]
        range_query_time = PerformanceAnalyzer.measure_range_query_time(db_bplus, table_name, ranges)
        bplus_times.append(range_query_time)

        db_brute = Database(db_name)
        db_brute.create_table(table_name, list(rows[0].keys()), primary_key="id", index_type="bruteforce")
        db_brute.insert_bulk(table_name, rows)

        range_query_time = PerformanceAnalyzer.measure_range_query_time(db_brute, table_name, ranges)
        brute_times.append(range_query_time)

    return test_sizes, bplus_times, brute_times

def measure_deletion_performance(table_name,db_name):
    test_sizes = generate_test_sizes()
    bplus_times = []
    brute_times = []

    for num_rows in test_sizes:
        print(f"Deletion: {num_rows} rows for {table_name}")
        rows = create_rows(table_name, num_rows)

        db_bplus = Database(db_name)
        db_bplus.create_table(table_name, list(rows[0].keys()), primary_key="id", index_type="bplustree")
        db_bplus.insert_bulk(table_name, rows)

        delete_ids = [1, num_rows // 2, num_rows]
        delete_time = PerformanceAnalyzer.measure_deletion_time(db_bplus, table_name, delete_ids)
        bplus_times.append(delete_time)

        db_brute = Database(db_name)
        db_brute.create_table(table_name, list(rows[0].keys()), primary_key="id", index_type="bruteforce")
        db_brute.insert_bulk(table_name, rows)

        delete_time = PerformanceAnalyzer.measure_deletion_time(db_brute, table_name, delete_ids)
        brute_times.append(delete_time)

    return test_sizes, bplus_times, brute_times

import os
import matplotlib.pyplot as plt

def plot_performance(sizes, bplus_times, brute_times, operation, table_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sizes, bplus_times, label='B+ Tree Time', marker='o')
    ax.plot(sizes, brute_times, label='Brute Force Time', marker='x')
    ax.set_xlabel('Number of Records')
    ax.set_ylabel('Time (ms)')
    ax.set_title(f'{operation} Time Performance ({table_name.title()} Table)')
    ax.legend()
    ax.grid(True)

    # Create a folder inside static if it doesn't exist
    save_dir = os.path.join('static', 'performance_plots')
    os.makedirs(save_dir, exist_ok=True)

    # Save the figure
    save_path = os.path.join(save_dir, f'{table_name}_{operation.lower()}_times.png')
    plt.savefig(save_path)
    print(f"Saved: {save_path}")
    plt.close(fig)


# Example usage
if __name__ == "__main__":
    table_name = "students"  # or "staff"

    # # # Measure and plot insertion
    # sizes, bplus_times, brute_times = measure_insertion_performance("students")
    # plot_performance(sizes, bplus_times, brute_times, "Insertion", "students")

    # # Measure and plot search
    # sizes, bplus_times, brute_times = measure_search_performance(table_name)
    # plot_performance(sizes, bplus_times, brute_times, "Search", table_name)

    # # Measure and plot range query
    # sizes, bplus_times, brute_times = measure_range_query_performance(table_name)
    # plot_performance(sizes, bplus_times, brute_times, "Range_Query", table_name)

    # # Measure and plot deletion
    # sizes, bplus_times, brute_times = measure_deletion_performance(table_name)
    # plot_performance(sizes, bplus_times, brute_times, "Deletion", table_name)
