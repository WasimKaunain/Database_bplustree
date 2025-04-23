import pickle
from tables import Table
from bplustree import BPlusTree
from bruteforce import BruteForceDB
import os


class Database:
    def __init__(self, db_name):   # <-- Add optional db_name parameter
        self.tables = {}          # <-- Save database name
        self.name = db_name

    def create_table(self, name, columns, primary_key, index_type='bplustree', t = 3):
        if name in self.tables:
            raise ValueError("Table already exists")
        if index_type == 'bplustree':
            index = BPlusTree(t)
        elif index_type == 'bruteforce':
            index = BruteForceDB()
        else:
            raise ValueError("Unsupported index type")
        self.tables[name] = Table(name, columns, primary_key, index)

    def delete_table(self, name):
        """Delete a table from the database."""
        if name in self.tables:
            del self.tables[name]
            return True
        return False

    def list_tables(self):
        """Return a list of all table names in the database."""
        return list(self.tables.keys())

    def insert(self, table_name, row):
        self.tables[table_name].insert(row)

    def insert_bulk(self, table_name, rows):
        for row in rows:
            self.tables[table_name].insert(row)

    def update(self, table_name, key, updates):
        return self.tables[table_name].update(key, updates)

    def delete(self, table_name, key):
        return self.tables[table_name].delete(key)

    def search(self, table_name, key):
        return self.tables[table_name].search(key)
    
    def delete_all_records(self,table_name):
        return self.tables[table_name].delete_all_records()

    def range_query(self, table_name, start, end):
        return self.tables[table_name].range_query(start, end)

    def aggregate(self, table_name, column, func):
        table = self.tables[table_name]
        values = [row[column] for row in table.rows.values() if column in row]
        if func == 'sum':
            return sum(values)
        elif func == 'avg':
            return sum(values) / len(values)
        elif func == 'max':
            return max(values)
        elif func == 'min':
            return min(values)
        else:
            raise ValueError("Unsupported aggregate function")
        
    def print_records(self, table_name):
        return self.tables[table_name].print_all_records()

    def save_database(self, filename):
        """Save the entire database to a file."""
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_database(filename):
        """Load the database from a file."""
        with open(filename, 'rb') as f:
            return pickle.load(f)
        
