# Source: https://github.com/emilydolson/python-red-black-trees/blob/main/src/rbtree.py

import sys
from typing import Type, TypeVar, Iterator


T = TypeVar('T', bound='Node')


# Node creation
class Node():

    def __init__(self: T, key: int) -> None:
        self._key = key
        self.parent = None
        self.left = None
        self.right = None
        self._color = 1
        self.value = None

    def __repr__(self: T) -> str:
        return "Key: " + str(self._key) + " Value: " + str(self.value)

    def get_color(self: T) -> str:
        return "black" if self._color == 0 else "red"

    def set_color(self: T, color: str) -> None:
        if color == "black":
            self._color = 0
        elif color == "red":
            self._color = 1
        else:
            raise Exception("Unknown color")

    def get_key(self: T) -> int:
        return self._key

    def is_red(self: T) -> bool:
        return self._color == 1

    def is_black(self: T) -> bool:
        return self._color == 0

    def is_null(self: T) -> bool:
        return self._key is None

    def depth(self: T) -> int:
        return 0 if self.parent is None else self.parent.depth() + 1

    @classmethod
    def null(cls: Type[T]) -> T:
        node = cls(0)
        node._key = None
        node.set_color("black")
        return node


T = TypeVar('T', bound='RedBlackTree')


class RedBlackTree():
    def __init__(self: T) -> None:
        self.TNULL = Node.null()
        self.root = self.TNULL
        self.size = 0
        self._iter_format = 0

    # Dunder Methods #
    def __iter__(self: T) -> Iterator:
        if self._iter_format == 0:
            return iter(self.preorder())
        if self._iter_format == 1:
            return iter(self.inorder())
        if self._iter_format == 2:
            return iter(self.postorder())

    def __getitem__(self: T, key: int) -> int:
        return self.search(key).value

    def __setitem__(self: T, key: int, value: int) -> None:
        self.search(key).value = value

    # Setters and Getters #
    def get_root(self: T) -> Node:
        return self.root

    def set_iteration_style(self: T, style: str) -> None:
        if style == "pre":
            self._iter_format = 0
        elif style == "in":
            self._iter_format = 1
        elif style == "post":
            self._iter_format = 2
        else:
            raise Exception("Unknown style.")

    # Copy method
    def copy(self: T) -> 'RedBlackTree':
        """
        Create a deep copy of the Red-Black Tree.
        Returns a new RedBlackTree with the same structure, colors, keys, and values.
        """
        new_tree = RedBlackTree()
        if self.root.is_null():
            return new_tree
        
        new_tree.root = self._copy_subtree(self.root, new_tree.TNULL)
        new_tree.size = self.size
        new_tree._iter_format = self._iter_format
        
        return new_tree
    
    def _copy_subtree(self: T, node: Node, parent: Node) -> Node:
        """
        Helper method to recursively copy a subtree.
        """
        if node.is_null():
            return self.TNULL
        
        # Create new node with same key and value
        new_node = Node(node.get_key())
        new_node.value = node.value
        new_node.set_color(node.get_color())
        new_node.parent = parent
        
        # Recursively copy left and right subtrees
        new_node.left = self._copy_subtree(node.left, new_node)
        new_node.right = self._copy_subtree(node.right, new_node)
        
        return new_node

    # Iterators #
    def preorder(self: T) -> list:
        return self.pre_order_helper(self.root)

    def inorder(self: T) -> list:
        return self.in_order_helper(self.root)

    def postorder(self: T) -> list:
        return self.post_order_helper(self.root)

    def pre_order_helper(self: T, node: Node) -> list:
        """
        Perform a preorder tree traversal starting at the
        given node.
        """
        output = []
        if not node.is_null():
            left = self.pre_order_helper(node.left)
            right = self.pre_order_helper(node.right)
            output.extend([node])
            output.extend(left)
            output.extend(right)
        return output

    def in_order_helper(self: T, node: Node) -> list:
        """
        Perform a inorder tree traversal starting at the
        given node.
        """
        output = []
        if not node.is_null():
            left = self.in_order_helper(node.left)
            right = self.in_order_helper(node.right)
            output.extend(left)
            output.extend([node])
            output.extend(right)
        return output

    def post_order_helper(self: T, node: Node) -> list:
        output = []
        if not node.is_null():
            left = self.post_order_helper(node.left)
            right = self.post_order_helper(node.right)
            output.extend(left)
            output.extend(right)
            output.extend([node])
        return output

    # Search the tree
    def search_tree_helper(self: T, node: Node, key: int) -> Node:
        if node.is_null() or key == node.get_key():
            return node

        if key < node.get_key():
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    # Balancing the tree after deletion
    def delete_fix(self: T, x: Node) -> None:
        while x != self.root and x.is_black():
            if x == x.parent.left:
                s = x.parent.right
                if s.is_red():
                    s.set_color("black")
                    x.parent.set_color("red")
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.is_black() and s.right.is_black():
                    s.set_color("red")
                    x = x.parent
                else:
                    if s.right.is_black():
                        s.left.set_color("black")
                        s.set_color("red")
                        self.right_rotate(s)
                        s = x.parent.right

                    s.set_color(x.parent.get_color())
                    x.parent.set_color("black")
                    s.right.set_color("black")
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.is_red():
                    s.set_color("black")
                    x.parent.set_color("red")
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.is_black() and s.right.is_black():
                    s.set_color("red")
                    x = x.parent
                else:
                    if s.left.is_black():
                        s.right.set_color("black")
                        s.set_color("red")
                        self.left_rotate(s)
                        s = x.parent.left

                    s.set_color(x.parent.get_color())
                    x.parent.set_color("black")
                    s.left.set_color("black")
                    self.right_rotate(x.parent)
                    x = self.root
        x.set_color("black")

    def __rb_transplant(self: T, u: Node, v: Node) -> None:
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Node deletion
    def delete_node_helper(self: T, node: Node, key: int) -> None:
        z = self.TNULL
        while not node.is_null():
            if node.get_key() == key:
                z = node

            if node.get_key() <= key:
                node = node.right
            else:
                node = node.left

        if z.is_null():
            # print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.get_color()
        if z.left.is_null():
            # If no left child, just scoot the right subtree up
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right.is_null()):
            # If no right child, just scoot the left subtree up
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.get_color()
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.set_color(z.get_color())
        if y_original_color == "black":
            self.delete_fix(x)

        self.size -= 1

    # Balance the tree after insertion
    def fix_insert(self: T, node: Node) -> None:
        while node.parent.is_red():
            if node.parent == node.parent.parent.right:
                u = node.parent.parent.left
                if u.is_red():
                    u.set_color("black")
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    self.left_rotate(node.parent.parent)
            else:
                u = node.parent.parent.right

                if u.is_red():
                    u.set_color("black")
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    self.right_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.set_color("black")

    # Printing the tree
    def __print_helper(self: T, node: Node, indent: str, last: bool) -> None:
        if not node.is_null():
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----  ")
                indent += "     "
            else:
                sys.stdout.write("L----   ")
                indent += "|    "

            s_color = "RED" if node.is_red() else "BLACK"
            print(str(node.get_key()) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def search(self: T, key: int) -> Node:
        return self.search_tree_helper(self.root, key)

    def minimum(self: T, node: Node = None) -> Node:
        if node is None:
            node = self.root
        if node.is_null():
            return self.TNULL
        while not node.left.is_null():
            node = node.left
        return node

    def maximum(self: T, node: Node = None) -> Node:
        if node is None:
            node = self.root
        if node.is_null():
            return self.TNULL
        while not node.right.is_null():
            node = node.right
        return node

    def successor(self: T, x: Node) -> Node:
        if not x.right.is_null():
            return self.minimum(x.right)

        y = x.parent
        while not y.is_null() and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self: T,  x: Node) -> Node:
        if (not x.left.is_null()):
            return self.maximum(x.left)

        y = x.parent
        while not y.is_null() and x == y.left:
            x = y
            y = y.parent

        return y

    def left_rotate(self: T, x: Node) -> None:
        y = x.right
        x.right = y.left
        if not y.left.is_null():
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self: T, x: Node) -> None:
        y = x.left
        x.left = y.right
        if not y.right.is_null():
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self: T, key: int) -> None:
        node = Node(key)
        node.left = self.TNULL
        node.right = self.TNULL
        node.set_color("red")

        y = None
        x = self.root

        while not x.is_null():
            y = x
            if node.get_key() < x.get_key():
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.get_key() < y.get_key():
            y.left = node
        else:
            y.right = node

        self.size += 1

        if node.parent is None:
            node.set_color("black")
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def delete(self: T, key: int) -> None:
        self.delete_node_helper(self.root, key)

    def print_tree(self: T) -> None:
        self.__print_helper(self.root, "", True)


if __name__ == "__main__":
    print("=== Testes da Red-Black Tree com método copy ===\n")
    
    # Teste 1: Cópia de árvore vazia
    print("1. Teste: Cópia de árvore vazia")
    empty_tree = RedBlackTree()
    empty_copy = empty_tree.copy()
    print(f"Árvore original vazia: {empty_tree.size == 0}")
    print(f"Cópia vazia: {empty_copy.size == 0}")
    print(f"São objetos diferentes: {empty_tree is not empty_copy}")
    print()
    
    # Teste 2: Cópia de árvore com um elemento
    print("2. Teste: Cópia de árvore com um elemento")
    single_tree = RedBlackTree()
    single_tree.insert(10)
    single_tree[10] = 100  # Definir valor
    
    single_copy = single_tree.copy()
    
    print(f"Árvore original - tamanho: {single_tree.size}, raiz: {single_tree.root.get_key()}")
    print(f"Cópia - tamanho: {single_copy.size}, raiz: {single_copy.root.get_key()}")
    print(f"Valor original: {single_tree[10]}")
    print(f"Valor cópia: {single_copy[10]}")
    print(f"Cor da raiz original: {single_tree.root.get_color()}")
    print(f"Cor da raiz cópia: {single_copy.root.get_color()}")
    print()
    
    # Teste 3: Cópia de árvore complexa
    print("3. Teste: Cópia de árvore complexa")
    complex_tree = RedBlackTree()
    keys = [20, 10, 30, 5, 15, 25, 35, 1, 8, 12, 18]
    
    for key in keys:
        complex_tree.insert(key)
        complex_tree[key] = key * 10  # Valor = chave * 10
    
    print(f"Árvore original inserida com chaves: {keys}")
    print(f"Tamanho da árvore original: {complex_tree.size}")
    
    complex_copy = complex_tree.copy()
    print(f"Tamanho da cópia: {complex_copy.size}")
    print()
    
    # Teste 4: Verificar independência das cópias
    print("4. Teste: Verificar independência das cópias")
    # Modificar a árvore original
    complex_tree.insert(40)
    complex_tree[10] = 999  # Alterar valor existente
    
    print(f"Após inserir 40 na original:")
    print(f"Tamanho original: {complex_tree.size}")
    print(f"Tamanho cópia: {complex_copy.size}")
    print(f"Valor de key=10 na original: {complex_tree[10]}")
    print(f"Valor de key=10 na cópia: {complex_copy[10]}")
    
    # Tentar buscar 40 nas duas árvores
    original_search = complex_tree.search(40)
    copy_search = complex_copy.search(40)
    
    print(f"Busca por 40 na original encontrada: {not original_search.is_null()}")
    print(f"Busca por 40 na cópia encontrada: {not copy_search.is_null()}")
    print()
    
    # Teste 5: Verificar estrutura e cores
    print("5. Teste: Verificar estrutura e cores")
    
    def compare_trees(tree1, tree2, node1, node2):
        """Compara recursivamente se duas árvores têm a mesma estrutura e cores"""
        if node1.is_null() and node2.is_null():
            return True
        
        if node1.is_null() or node2.is_null():
            return False
            
        if (node1.get_key() != node2.get_key() or 
            node1.get_color() != node2.get_color()):
            return False
            
        return (compare_trees(tree1, tree2, node1.left, node2.left) and
                compare_trees(tree1, tree2, node1.right, node2.right))
    
    # Criar uma nova árvore para comparação limpa
    test_tree = RedBlackTree()
    for key in [20, 10, 30, 5, 15, 25, 35]:
        test_tree.insert(key)
    
    test_copy = test_tree.copy()
    
    structure_match = compare_trees(test_tree, test_copy, test_tree.root, test_copy.root)
    print(f"Estruturas e cores idênticas: {structure_match}")
    print()
    
    # Teste 6: Testar diferentes estilos de iteração
    print("6. Teste: Estilos de iteração preservados")
    iter_tree = RedBlackTree()
    for key in [20, 10, 30]:
        iter_tree.insert(key)
    
    # Testar diferentes estilos
    styles = ["pre", "in", "post"]
    for style in styles:
        iter_tree.set_iteration_style(style)
        iter_copy = iter_tree.copy()
        
        original_keys = [node.get_key() for node in iter_tree]
        copy_keys = [node.get_key() for node in iter_copy]
        
        print(f"Estilo {style} - Original: {original_keys}")
        print(f"Estilo {style} - Cópia: {copy_keys}")
        print(f"Iterações idênticas: {original_keys == copy_keys}")
    
    print()
    
    # Teste 7: Teste de performance com árvore maior
    print("7. Teste: Performance com árvore maior")
    import time
    
    big_tree = RedBlackTree()
    keys = list(range(1, 101))  # 100 elementos
    
    for key in keys:
        big_tree.insert(key)
        big_tree[key] = key * key
    
    start_time = time.time()
    big_copy = big_tree.copy()
    end_time = time.time()
    
    print(f"Cópia de árvore com {big_tree.size} elementos")
    print(f"Tempo de cópia: {end_time - start_time:.6f} segundos")
    print(f"Tamanhos iguais: {big_tree.size == big_copy.size}")
    
    # Verificar alguns valores aleatórios
    test_keys = [1, 25, 50, 75, 100]
    values_match = all(big_tree[key] == big_copy[key] for key in test_keys)
    print(f"Valores correspondentes: {values_match}")
    
    print("\n=== Todos os testes concluídos ===")