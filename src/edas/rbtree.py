# class to implement node of RB Tree
class RBNode:
        # cnostructor
    def __init__(self, value, color='red'):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    # function to get the grandparent of node
    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    # function to get the sibling of node
    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

    # function to get the uncle of node
    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()

# function to implement Red Black Tree


class RedBlackTree:
        # constructor to initialize the RB tree
    def __init__(self):
        self.root = None

    # function to search a value in RB Tree
    def search(self, value):
        curr_node = self.root
        while curr_node is not None:
            if value == curr_node.value:
                return curr_node
            elif value < curr_node.value:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        return None

    # function to insert a node in RB Tree, similar to BST insertion
    def insert(self, value):
        # Regular insertion
        new_node = RBNode(value)
        if self.root is None:
            self.root = new_node
        else:
            curr_node = self.root
            while True:
                if value < curr_node.value:
                    if curr_node.left is None:
                        curr_node.left = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.left
                else:
                    if curr_node.right is None:
                        curr_node.right = new_node
                        new_node.parent = curr_node
                        break
                    else:
                        curr_node = curr_node.right
        self.insert_fix(new_node)

    # Function to fix RB tree properties after insertion
    def insert_fix(self, new_node):
        while new_node.parent and new_node.parent.color == 'red':
            if new_node.parent == new_node.grandparent().left:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_right(new_node.grandparent())
            else:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_left(new_node.grandparent())
        self.root.color = 'black'

    # function to delete a value from RB Tree
    def delete(self, value):
        node_to_remove = self.search(value)

        if node_to_remove is None:
            return

        original_color = node_to_remove.color
        fixup_node = None
        fixup_parent = None
        
        if node_to_remove.left is None:
            fixup_node = node_to_remove.right
            fixup_parent = node_to_remove.parent
            self._replace_node(node_to_remove, fixup_node)
        elif node_to_remove.right is None:
            fixup_node = node_to_remove.left
            fixup_parent = node_to_remove.parent
            self._replace_node(node_to_remove, fixup_node)
        else:
            successor = self._find_min(node_to_remove.right)
            original_color = successor.color
            fixup_node = successor.right
            
            if successor.parent == node_to_remove:
                fixup_parent = successor
            else:
                fixup_parent = successor.parent
                self._replace_node(successor, successor.right)
                successor.right = node_to_remove.right
                successor.right.parent = successor
            
            self._replace_node(node_to_remove, successor)
            successor.left = node_to_remove.left
            successor.left.parent = successor
            successor.color = node_to_remove.color

        if original_color == 'black':
            self.delete_fix(fixup_node, fixup_parent)

    # function to fix RB Tree properties after deletion
    def delete_fix(self, x, x_parent):
        while x != self.root and (x is None or x.color == 'black'):
            if x_parent is None:
                break
                
            if x == x_parent.left or (x is None and x_parent.left is None):
                sibling = x_parent.right
                
                # Case 1: Sibling is red
                if sibling and sibling.color == 'red':
                    sibling.color = 'black'
                    x_parent.color = 'red'
                    self.rotate_left(x_parent)
                    sibling = x_parent.right
                
                if sibling is None:
                    x = x_parent
                    x_parent = x.parent
                    continue
                    
                # Case 2: Sibling is black and both children are black
                left_black = sibling.left is None or sibling.left.color == 'black'
                right_black = sibling.right is None or sibling.right.color == 'black'
                
                if left_black and right_black:
                    sibling.color = 'red'
                    x = x_parent
                    x_parent = x.parent
                else:
                    # Case 3: Sibling is black, left child is red, right child is black
                    if right_black:
                        if sibling.left:
                            sibling.left.color = 'black'
                        sibling.color = 'red'
                        self.rotate_right(sibling)
                        sibling = x_parent.right
                    
                    # Case 4: Sibling is black, right child is red
                    if sibling:
                        sibling.color = x_parent.color
                        x_parent.color = 'black'
                        if sibling.right:
                            sibling.right.color = 'black'
                        self.rotate_left(x_parent)
                    x = self.root
            else:
                sibling = x_parent.left
                
                # Case 1: Sibling is red
                if sibling and sibling.color == 'red':
                    sibling.color = 'black'
                    x_parent.color = 'red'
                    self.rotate_right(x_parent)
                    sibling = x_parent.left
                
                if sibling is None:
                    x = x_parent
                    x_parent = x.parent
                    continue
                    
                # Case 2: Sibling is black and both children are black
                left_black = sibling.left is None or sibling.left.color == 'black'
                right_black = sibling.right is None or sibling.right.color == 'black'
                
                if left_black and right_black:
                    sibling.color = 'red'
                    x = x_parent
                    x_parent = x.parent
                else:
                    # Case 3: Sibling is black, right child is red, left child is black
                    if left_black:
                        if sibling.right:
                            sibling.right.color = 'black'
                        sibling.color = 'red'
                        self.rotate_left(sibling)
                        sibling = x_parent.left
                    
                    # Case 4: Sibling is black, left child is red
                    if sibling:
                        sibling.color = x_parent.color
                        x_parent.color = 'black'
                        if sibling.left:
                            sibling.left.color = 'black'
                        self.rotate_right(x_parent)
                    x = self.root
        
        if x:
            x.color = 'black'

    # Function for left rotation of RB Tree
    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child

    # function for right rotation of RB Tree
    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child

    # function to replace an old node with a new node
    def _replace_node(self, old_node, new_node):
        if old_node.parent is None:
            self.root = new_node
        else:
            if old_node == old_node.parent.left:
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
        if new_node is not None:
            new_node.parent = old_node.parent

    # function to find node with minimum value in a subtree
    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    # function to perform inorder traversal
    def _inorder_traversal(self, node):
        if node is not None:
            self._inorder_traversal(node.left)
            print(node.value, end=" ")
            self._inorder_traversal(node.right)

    # function to copy the tree
    def copy(self):
        """Creates a deep copy of the Red-Black Tree"""
        new_tree = RedBlackTree()
        if self.root is None:
            return new_tree
        
        # Helper function to recursively copy nodes
        def copy_node(original_node, parent=None):
            if original_node is None:
                return None
            
            # Create new node with same value and color
            new_node = RBNode(original_node.value, original_node.color)
            new_node.parent = parent
            
            # Recursively copy left and right subtrees
            new_node.left = copy_node(original_node.left, new_node)
            new_node.right = copy_node(original_node.right, new_node)
            
            return new_node
        
        new_tree.root = copy_node(self.root)
        return new_tree

    # Helper method to get all values in order
    def get_inorder_values(self):
        """Returns list of values in inorder traversal"""
        values = []
        def inorder_helper(node):
            if node is not None:
                inorder_helper(node.left)
                values.append(node.value)
                inorder_helper(node.right)
        
        inorder_helper(self.root)
        return values

    # Helper method to validate RB tree properties
    def is_valid_rb_tree(self):
        """Validates if the tree maintains Red-Black tree properties"""
        if self.root is None:
            return True
        
        # Property 1: Root is black
        if self.root.color != 'black':
            return False
        
        # Property 2: All leaves are black (NULL nodes are considered black)
        # Property 3: Red nodes have black children
        # Property 4: All paths have same black height
        def validate_helper(node):
            if node is None:
                return True, 1  # NULL nodes are black with height 1
            
            # Check if red node has red children
            if node.color == 'red':
                if (node.left and node.left.color == 'red') or \
                   (node.right and node.right.color == 'red'):
                    return False, 0
            
            # Recursively validate subtrees
            left_valid, left_black_height = validate_helper(node.left)
            right_valid, right_black_height = validate_helper(node.right)
            
            # Check if both subtrees are valid and have same black height
            if not left_valid or not right_valid or left_black_height != right_black_height:
                return False, 0
            
            # Calculate black height for current node
            current_black_height = left_black_height
            if node.color == 'black':
                current_black_height += 1
            
            return True, current_black_height
        
        valid, _ = validate_helper(self.root)
        return valid


# Comprehensive test suite
if __name__ == "__main__":
    print("=" * 60)
    print("COMPREHENSIVE RED-BLACK TREE TESTS")
    print("=" * 60)

    # Test 1: Basic insertion and structure
    print("\n1. Testing basic insertion and inorder traversal:")
    tree = RedBlackTree()
    values = [10, 20, 30, 40, 50, 25]
    
    for val in values:
        tree.insert(val)
        print(f"Inserted {val}, tree valid: {tree.is_valid_rb_tree()}")
    
    print("Inorder traversal:", tree.get_inorder_values())
    
    # Test 2: Copy method
    print("\n2. Testing copy method:")
    tree_copy = tree.copy()
    print("Original tree inorder:", tree.get_inorder_values())
    print("Copied tree inorder:", tree_copy.get_inorder_values())
    print(f"Copy is valid RB tree: {tree_copy.is_valid_rb_tree()}")
    
    # Verify independence of copy
    tree_copy.insert(15)
    print("After inserting 15 in copy:")
    print("Original tree:", tree.get_inorder_values())
    print("Copied tree:", tree_copy.get_inorder_values())

    # Test 3: Deletion tests
    print("\n3. Testing deletion operations:")
    test_tree = tree.copy()
    
    # Delete leaf node
    print("Deleting leaf node (50):")
    test_tree.delete(50)
    print("After deletion:", test_tree.get_inorder_values())
    print(f"Tree valid: {test_tree.is_valid_rb_tree()}")
    
    # Delete node with one child
    test_tree.insert(35)
    print("Added 35, then deleting node with one child (40):")
    test_tree.delete(40)
    print("After deletion:", test_tree.get_inorder_values())
    print(f"Tree valid: {test_tree.is_valid_rb_tree()}")
    
    # Delete node with two children
    print("Deleting node with two children (30):")
    test_tree.delete(30)
    print("After deletion:", test_tree.get_inorder_values())
    print(f"Tree valid: {test_tree.is_valid_rb_tree()}")

    # Test 4: Search functionality
    print("\n4. Testing search functionality:")
    search_tree = RedBlackTree()
    for val in [15, 10, 20, 8, 12, 25]:
        search_tree.insert(val)
    
    test_values = [10, 15, 99, 8, 100]
    for val in test_values:
        result = search_tree.search(val)
        print(f"Search for {val}: {'Found' if result else 'Not found'}")

    # Test 5: Edge cases
    print("\n5. Testing edge cases:")
    
    # Empty tree operations
    empty_tree = RedBlackTree()
    print(f"Empty tree valid: {empty_tree.is_valid_rb_tree()}")
    print(f"Search in empty tree: {empty_tree.search(10)}")
    empty_tree.delete(10)  # Should not crash
    print("Delete from empty tree: OK")
    
    # Copy empty tree
    empty_copy = empty_tree.copy()
    print(f"Empty tree copy valid: {empty_copy.is_valid_rb_tree()}")
    
    # Single node tree
    single_tree = RedBlackTree()
    single_tree.insert(42)
    print(f"Single node tree valid: {single_tree.is_valid_rb_tree()}")
    print(f"Root color: {single_tree.root.color}")
    
    single_copy = single_tree.copy()
    print(f"Single node copy valid: {single_copy.is_valid_rb_tree()}")
    print(f"Copy root color: {single_copy.root.color}")

    # Test 6: Stress test with sequential insertions
    print("\n6. Stress test - sequential insertions:")
    stress_tree = RedBlackTree()
    for i in range(1, 16):
        stress_tree.insert(i)
    
    print("Sequential insertions 1-15:")
    print("Inorder:", stress_tree.get_inorder_values())
    print(f"Tree valid: {stress_tree.is_valid_rb_tree()}")
    
    # Test copy of stress tree
    stress_copy = stress_tree.copy()
    print(f"Stress tree copy valid: {stress_copy.is_valid_rb_tree()}")

    # Test 7: Stress test with deletions
    print("\n7. Stress test - multiple deletions:")
    delete_values = [1, 3, 5, 7, 9, 11, 13, 15]
    for val in delete_values:
        stress_tree.delete(val)
        print(f"Deleted {val}, remaining: {stress_tree.get_inorder_values()}, valid: {stress_tree.is_valid_rb_tree()}")

    # Test 8: Random order insertions
    print("\n8. Testing random order insertions:")
    import random
    random_tree = RedBlackTree()
    random_values = list(range(1, 21))
    random.shuffle(random_values)
    
    print(f"Inserting in random order: {random_values}")
    for val in random_values:
        random_tree.insert(val)
    
    print("Final inorder:", random_tree.get_inorder_values())
    print(f"Random tree valid: {random_tree.is_valid_rb_tree()}")
    
    # Copy and verify
    random_copy = random_tree.copy()
    print(f"Random tree copy valid: {random_copy.is_valid_rb_tree()}")

    # Test 9: Duplicate insertion handling
    print("\n9. Testing duplicate insertions:")
    dup_tree = RedBlackTree()
    test_vals = [5, 3, 7, 3, 5, 9, 7]  # Contains duplicates
    
    for val in test_vals:
        dup_tree.insert(val)
    
    print(f"After inserting {test_vals}:")
    print("Inorder:", dup_tree.get_inorder_values())
    print(f"Tree valid: {dup_tree.is_valid_rb_tree()}")

    # Test 10: Delete non-existent values
    print("\n10. Testing deletion of non-existent values:")
    test_tree = RedBlackTree()
    for val in [10, 5, 15]:
        test_tree.insert(val)
    
    print("Before deletion:", test_tree.get_inorder_values())
    test_tree.delete(100)  # Non-existent
    print("After deleting 100 (non-existent):", test_tree.get_inorder_values())
    print(f"Tree still valid: {test_tree.is_valid_rb_tree()}")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)