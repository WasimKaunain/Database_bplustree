from bplustree import BPlusTree
import os

# Create a B+ Tree of order 4
tree = BPlusTree(t=4)

# Insert some (key, value) pairs
tree.insert(5, "A")
tree.insert(10, "B")
tree.insert(15, "C")
tree.insert(20, "D")
tree.insert(25, "E")
tree.insert(30, "F")

# # Search for a key
# print("Search 15:", tree.search(15))  # Should print "C"

# # Range query between 10 and 25
# print("Range 10-25:", tree.range_query(10, 25))  # Should print keys and values between 10 and 25

# # Delete a key
# tree.delete(15)
# print("After deleting 15, search 15:", tree.search(15))  # Should print None

visualize_folder = 'visualize'
if not os.path.exists(visualize_folder):
    os.makedirs(visualize_folder)

# Visualize the tree (creates tree.png file)
tree.visualize(os.path.join(visualize_folder,'tree.png'))
print("Tree visualization saved in 'visualize/tree.png'.")
