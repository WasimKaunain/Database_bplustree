import pickle  # For save/load

class Table:
    def __init__(self, name, columns, primary_key, index):
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        self.rows = {}
        self.index = index  # Must be called bplustree (even if brute-force)

    def insert(self, row):
        key = row[self.primary_key]
        if key in self.rows:
            raise ValueError("Duplicate primary key")
        self.rows[key] = row
        self.index.insert(key, row)

    def update(self,key,updates):
        if key in self.rows:
            for k, v in updates.items():
                self.rows[key][k] = v
        else:
            raise KeyError("Key not found")

    def delete(self, key):
        if key in self.rows:
            del self.rows[key]
            self.index.delete(key)
            return True
        return False
    
    def delete_all_records(self):
        self.rows.clear()
        self.index.clear()

    def search(self, key):
        return self.index.search(key)

    def range_query(self, start, end):
        return self.index.range_query(start, end)
    
    def print_all_records(self):
        if not self.rows:
            print(f"No records found in table '{self.name}'")
        else:
            records = {}
            print(f"Records in table '{self.name}':")
            for key, record in self.rows.items():
                records[key] = record
            return records

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
