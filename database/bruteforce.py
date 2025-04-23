class BruteForceDB:
    def __init__(self):
        self.records = []  # List to store (key, value) tuples

    def insert(self, key, value):
        self.records.append((key, value))

    def search(self, key):
        for k, v in self.records:
            if k == key:
                return v
        return None
    

    def delete(self, key):
        for i, (k, v) in enumerate(self.records):
            if k == key:
                del self.records[i]
                return True
        return False

    def range_query(self, start_key, end_key):
        result = []
        for k, v in self.records:
            if start_key <= k <= end_key:
                result.append((k, v))
        result.sort(key=lambda x: x[0])  # Sort by key
        return result
