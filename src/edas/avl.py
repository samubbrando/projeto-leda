from collections import deque

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0  # altura do nó

    def update_height(self):
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        self.height = 1 + max(left_height, right_height)

    def balance_factor(self):
        left_height = self.left.height if self.left else -1
        right_height = self.right.height if self.right else -1
        return left_height - right_height

class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0

    # ------------------ Inserção ------------------
    def add(self, value):
        self.root = self._add(self.root, value)
        self.root.parent = None
        self.size += 1

    def _add(self, node, value):
        if node is None:
            return Node(value)

        if value < node.value:
            node.left = self._add(node.left, value)
            node.left.parent = node
        else:
            node.right = self._add(node.right, value)
            node.right.parent = node

        node.update_height()
        return self._balance(node)

    # ------------------ Remoção ------------------
    def remove(self, value):
        if self.root:
            self.root = self._remove(self.root, value)
            if self.root:
                self.root.parent = None
            self.size -= 1

    def _remove(self, node, value):
        if node is None:
            return None

        if value < node.value:
            node.left = self._remove(node.left, value)
            if node.left:
                node.left.parent = node
        elif value > node.value:
            node.right = self._remove(node.right, value)
            if node.right:
                node.right.parent = node
        else:
            # Nó encontrado
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Nó com dois filhos: substitui pelo sucessor
                succ = self._min(node.right)
                node.value = succ.value
                node.right = self._remove(node.right, succ.value)
                if node.right:
                    node.right.parent = node

        node.update_height()
        return self._balance(node)

    # ------------------ Rotação e balanceamento ------------------
    def _balance(self, node):
        bf = node.balance_factor()
        # Rotação direita
        if bf > 1 and node.left.balance_factor() >= 0:
            return self._rotate_right(node)
        # Rotação esquerda
        if bf < -1 and node.right.balance_factor() <= 0:
            return self._rotate_left(node)
        # Rotação esquerda-direita
        if bf > 1 and node.left.balance_factor() < 0:
            node.left = self._rotate_left(node.left)
            node.left.parent = node
            return self._rotate_right(node)
        # Rotação direita-esquerda
        if bf < -1 and node.right.balance_factor() > 0:
            node.right = self._rotate_right(node.right)
            node.right.parent = node
            return self._rotate_left(node)
        return node

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        y.parent = z.parent
        z.parent = y
        z.right = T2
        if T2:
            T2.parent = z

        z.update_height()
        y.update_height()
        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        y.parent = z.parent
        z.parent = y
        z.left = T3
        if T3:
            T3.parent = z

        z.update_height()
        y.update_height()
        return y

    # ------------------ Min / Max ------------------
    def _min(self, node):
        while node.left:
            node = node.left
        return node

    def min(self):
        return self._min(self.root) if self.root else None

    def _max(self, node):
        while node.right:
            node = node.right
        return node

    def max(self):
        return self._max(self.root) if self.root else None

    # ------------------ Search ------------------
    def search(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if not node:
            return None
        if node.value == value:
            return node
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    # ------------------ Predecessor / Sucessor ------------------
    def predecessor(self, node):
        if node.left:
            return self._max(node.left)
        parent = node.parent
        while parent and node == parent.left:
            node = parent
            parent = parent.parent
        return parent

    def sucessor(self, node):
        if node.right:
            return self._min(node.right)
        parent = node.parent
        while parent and node == parent.right:
            node = parent
            parent = parent.parent
        return parent

    # ------------------ Percursos ------------------
    def in_order(self):
        self._in_order(self.root)

    def _in_order(self, node):
        if node:
            self._in_order(node.left)
            print(node.value)
            self._in_order(node.right)

    def pre_order(self):
        self._pre_order(self.root)

    def _pre_order(self, node):
        if node:
            print(node.value)
            self._pre_order(node.left)
            self._pre_order(node.right)

    def pos_order(self):
        self._pos_order(self.root)

    def _pos_order(self, node):
        if node:
            self._pos_order(node.left)
            self._pos_order(node.right)
            print(node.value)

    # ------------------ BFS ------------------
    def bfs(self):
        result = []
        if not self.root:
            return result
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    # ------------------ Util ------------------
    def height(self):
        return self.root.height if self.root else -1

    def is_empty(self):
        return self.root is None

    def size_tree(self):
        return self.size
