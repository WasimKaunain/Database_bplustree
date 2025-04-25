from graphviz import Digraph

class BPlusTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.next = None  # For leaf node linking

class BPlusTree:
    def __init__(self, t=3):
        self.root = BPlusTreeNode(leaf=True)
        self.t = t
    def search(self, key, node=None):
        node = node or self.root
        if node.leaf:
            for k, v in node.keys:
                if k == key:
                    return v
            return None
        else:
            for i, item in enumerate(node.keys):
                if key < item:
                    return self.search(key, node.children[i])
            return self.search(key, node.children[-1])

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == self.t - 1:
            new_root = BPlusTreeNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        if node.leaf:
            node.keys.append((key, value))
            node.keys.sort(key=lambda x: x[0])
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent, index):
        t = self.t
        node = parent.children[index]
        mid = t // 2
        new_node = BPlusTreeNode(leaf=node.leaf)
        if node.leaf:
            new_node.keys = node.keys[mid:]
            node.keys = node.keys[:mid]
            new_node.next = node.next
            node.next = new_node
            parent.keys.insert(index, new_node.keys[0][0])
        else:
            parent.keys.insert(index, node.keys[mid])
            new_node.keys = node.keys[mid+1:]
            new_node.children = node.children[mid+1:]
            node.keys = node.keys[:mid]
            node.children = node.children[:mid+1]

        parent.children.insert(index + 1, new_node)

    def delete(self, key):
        self._delete(self.root, key)
        # If root has become empty and has a child, demote it
        if not self.root.leaf and len(self.root.keys) == 0:
            self.root = self.root.children[0]

    def _delete(self, node, key):
        if node.leaf:
            # Direct deletion from leaf
            for i, (k, v) in enumerate(node.keys):
                if k == key:
                    node.keys.pop(i)
                    return
        else:
            # Navigate to child that may contain the key
            idx = 0
            while idx < len(node.keys) and key > node.keys[idx]:
                idx += 1

            if idx >= len(node.children):
                return  # key not found

            self._delete(node.children[idx], key)

            # Fix underflow if it happened
            if len(node.children[idx].keys) < (self.t - 1):
                self._fix_underflow(node, idx)

            # Update parent key if smallest key in child has changed
            if not node.children[idx].leaf:
                # Ensure there are keys to borrow from the right sibling
                if idx < len(node.children) - 1 and len(node.children[idx + 1].keys) > 0:
                    node.keys[idx] = node.children[idx + 1].keys[0][0]
                elif idx > 0 and len(node.children[idx - 1].keys) > 0:
                    node.keys[idx - 1] = node.children[idx].keys[0][0]

    def _fix_underflow(self, parent, idx):
        t = self.t
        child = parent.children[idx]
    
        # Try borrowing from left sibling
        if idx > 0 and len(parent.children[idx - 1].keys) > t - 1:
            left = parent.children[idx - 1]
            if child.leaf:
                borrowed = left.keys.pop(-1)
                child.keys.insert(0, borrowed)
                parent.keys[idx - 1] = child.keys[0][0]
            else:
                child.keys.insert(0, parent.keys[idx - 1])
                parent.keys[idx - 1] = left.keys.pop(-1)
                child.children.insert(0, left.children.pop(-1))
    
        # Try borrowing from right sibling
        elif idx < len(parent.children) - 1 and len(parent.children[idx + 1].keys) > t - 1:
            right = parent.children[idx + 1]
            if child.leaf:
                borrowed = right.keys.pop(0)
                child.keys.append(borrowed)
                parent.keys[idx] = right.keys[0][0]
            else:
                child.keys.append(parent.keys[idx])
                parent.keys[idx] = right.keys.pop(0)
                child.children.append(right.children.pop(0))
    
        # Merge with sibling
        else:
            if idx > 0:
                left = parent.children[idx - 1]
                if child.leaf:
                    left.keys.extend(child.keys)
                    left.next = child.next
                else:
                    left.keys.append(parent.keys[idx - 1])
                    left.keys.extend(child.keys)
                    left.children.extend(child.children)
                parent.keys.pop(idx - 1)
                parent.children.pop(idx)
            elif idx < len(parent.children) - 1:  # Ensure idx is within range
                right = parent.children[idx + 1]
                if child.leaf:
                    child.keys.extend(right.keys)
                    child.next = right.next
                else:
                    child.keys.append(parent.keys[idx])
                    child.keys.extend(right.keys)
                    child.children.extend(right.children)
                parent.keys.pop(idx)
                parent.children.pop(idx + 1)


    def range_query(self, start_key, end_key):
        result = []
        node=self.root
        while not node.leaf:
            child_found=0
            for i, item in enumerate(node.keys):
                if start_key < item:
                     node=node.children[i]
                     child_found=1
                     break
            if child_found==0:
                node=node.children[-1]
        while node:
            breaker=0
            for k, v in node.keys:
                if start_key <= k <= end_key:
                    result.append((k, v))
                if(k>=end_key):
                    breaker=1
                    break
            node = node.next
            if(breaker==1):
                break
        return result

    def visualize(self, filename='bplustree'):
        dot = Digraph(format='png')  # Create a new Digraph instance for the visualization
        dot.attr(size='8,8')  # Set the size of the output image (optional)

        # Start the recursive node addition
        self._add_nodes(dot, self.root)

        # Render the graph to a file
        dot.render(filename, cleanup=True)
        print(f"B+ Tree visualization saved as {filename}.png")
        return dot

    def _add_nodes(self, dot, node, parent_id=None):
        # Create a unique ID for the current node
        node_id = str(id(node))
        
        # If the node is a leaf, color it differently for visualization
        if node.leaf:
            label = '|'.join(str(k) for k, _ in node.keys)  # Display only keys for leaf nodes
            dot.node(node_id, label=label, shape='record', style='filled', fillcolor='lightblue')
        else:
            label = '|'.join(str(k) for k in node.keys)  # Internal nodes will have keys as labels
            dot.node(node_id, label=label, shape='record', style='filled', fillcolor='lightgrey')

        # Connect parent node to the current node
        if parent_id:
            dot.edge(parent_id, node_id)

        # Add the child nodes recursively
        for child in node.children:
            self._add_nodes(dot, child, parent_id=node_id)

        # If this is a leaf node, add the next link to the next leaf node (leaf linkage)
        if node.leaf and node.next:
            dot.edge(node_id, str(id(node.next)), label="next", style="dashed")