import time
import tracemalloc

class PerformanceAnalyzer:
    @staticmethod
    def measure_insertion_time(db, table_name, data):
        start_time = time.perf_counter()
        for row in data:
            db.insert(table_name, row)
        end_time = time.perf_counter()
        return end_time - start_time

    @staticmethod
    def measure_search_time(db, table_name, keys):
        start_time = time.perf_counter()
        for key in keys:
            db.search(table_name, key)
        end_time = time.perf_counter()
        return end_time - start_time
    
    @staticmethod
    def measure_updation_time(db, table_name, updates):
        start_time = time.perf_counter()
        for key, update_data in updates:
            db.update(table_name, key, update_data)
        end_time = time.perf_counter()
        return end_time - start_time


    @staticmethod
    def measure_deletion_time(db, table_name, keys):
        start_time = time.perf_counter()
        for key in keys:
            db.delete(table_name, key)
        end_time = time.perf_counter()
        return end_time - start_time

    @staticmethod
    def measure_range_query_time(db, table_name, ranges):
        start_time = time.perf_counter()
        for start_key, end_key in ranges:
            db.range_query(table_name, start_key, end_key)
        end_time = time.perf_counter()
        return end_time - start_time

    @staticmethod
    def measure_memory_usage(db):
        tracemalloc.start()
        _ = db.tables  # Accessing to ensure memory is allocated
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return current, peak
