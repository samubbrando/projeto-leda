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

    # ------------------ Copy ------------------
    def copy(self):
        """
        Cria uma cópia profunda da árvore AVL.
        Retorna uma nova instância de AVLTree com os mesmos valores.
        """
        new_tree = AVLTree()
        if self.root:
            new_tree.root = self._copy_node(self.root)
            new_tree.size = self.size
        return new_tree

    def _copy_node(self, node):
        """
        Método auxiliar recursivo para copiar os nós da árvore.
        Cria um novo nó com o mesmo valor e copia recursivamente
        os filhos esquerdo e direito.
        """
        if not node:
            return None
        
        # Cria um novo nó com o mesmo valor
        new_node = Node(node.value)
        new_node.height = node.height
        
        # Copia recursivamente os filhos
        new_node.left = self._copy_node(node.left)
        new_node.right = self._copy_node(node.right)
        
        # Ajusta os ponteiros parent
        if new_node.left:
            new_node.left.parent = new_node
        if new_node.right:
            new_node.right.parent = new_node
            
        return new_node

    # ------------------ Util ------------------
    def height(self):
        return self.root.height if self.root else -1

    def is_empty(self):
        return self.root is None

    def size_tree(self):
        return self.size

    def to_list(self):
        """Converte a árvore em uma lista ordenada (in-order)"""
        result = []
        self._to_list(self.root, result)
        return result

    def _to_list(self, node, result):
        if node:
            self._to_list(node.left, result)
            result.append(node.value)
            self._to_list(node.right, result)


if __name__ == "__main__":
    print("=== Testes da AVL Tree com método copy ===\n")
    
    # Teste 1: Criação e inserção de elementos
    print("1. Testando inserção de elementos:")
    tree1 = AVLTree()
    valores = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 35]
    
    for valor in valores:
        tree1.add(valor)
    
    print(f"Árvore original - Tamanho: {tree1.size_tree()}")
    print(f"Altura: {tree1.height()}")
    print(f"BFS: {tree1.bfs()}")
    print(f"In-order: {tree1.to_list()}")
    print()
    
    # Teste 2: Testando o método copy
    print("2. Testando método copy:")
    tree2 = tree1.copy()
    
    print(f"Árvore copiada - Tamanho: {tree2.size_tree()}")
    print(f"Altura: {tree2.height()}")
    print(f"BFS: {tree2.bfs()}")
    print(f"In-order: {tree2.to_list()}")
    print()
    
    # Teste 3: Verificando independência das árvores
    print("3. Testando independência das árvores:")
    print("Adicionando 100 na árvore original...")
    tree1.add(100)
    print("Removendo 25 da árvore copiada...")
    tree2.remove(25)
    
    print(f"Árvore original - Tamanho: {tree1.size_tree()}, BFS: {tree1.bfs()}")
    print(f"Árvore copiada - Tamanho: {tree2.size_tree()}, BFS: {tree2.bfs()}")
    print()
    
    # Teste 4: Testando cópia de árvore vazia
    print("4. Testando cópia de árvore vazia:")
    tree_vazia = AVLTree()
    copia_vazia = tree_vazia.copy()
    
    print(f"Árvore vazia original - Tamanho: {tree_vazia.size_tree()}, Vazia: {tree_vazia.is_empty()}")
    print(f"Cópia da árvore vazia - Tamanho: {copia_vazia.size_tree()}, Vazia: {copia_vazia.is_empty()}")
    print()
    
    # Teste 5: Testando busca nas árvores copiadas
    print("5. Testando busca nas árvores:")
    valores_busca = [50, 25, 100, 999]
    
    for valor in valores_busca:
        resultado_orig = tree1.search(valor)
        resultado_copia = tree2.search(valor)
        
        print(f"Busca por {valor}:")
        print(f"  Original: {'Encontrado' if resultado_orig else 'Não encontrado'}")
        print(f"  Cópia: {'Encontrado' if resultado_copia else 'Não encontrado'}")
    
    print()
    
    # Teste 6: Testando min/max
    print("6. Testando min/max:")
    print(f"Árvore original - Min: {tree1.min().value if tree1.min() else None}, Max: {tree1.max().value if tree1.max() else None}")
    print(f"Árvore copiada - Min: {tree2.min().value if tree2.min() else None}, Max: {tree2.max().value if tree2.max() else None}")
    print()
    
    # Teste 7: Testando múltiplas cópias
    print("7. Testando múltiplas cópias:")
    tree3 = tree2.copy()
    tree4 = tree3.copy()
    
    tree3.add(200)
    tree4.add(300)
    
    print(f"Árvore 2 (original da cópia): {tree2.bfs()}")
    print(f"Árvore 3 (cópia + 200): {tree3.bfs()}")
    print(f"Árvore 4 (cópia da cópia + 300): {tree4.bfs()}")
    
    print("\n=== Todos os testes concluídos! ===")