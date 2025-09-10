from typing import Optional, List, Any
from random import random
import sys

class Node:
    """
    Um Node contém um par chave valor e um dicionário de Nodes a frente dele.
    A lógica é oferecer n opções de Nodes que ele pode acessar para que 
    caso você queira pular adiante, você selecione o Node que o leva mais
    para próximo do Node que você deseja.
    """

    def __init__(self, key: int, value: Any, level: int = 1):
        """
        Inicializa os valores, limitados a inteiros para chave e valor.

        Args:
            key (int): Chave que identifica o node
            value (Any): Valor do node
            level (int): Tamanho de layers que podem ser atribuídos ao Node
        """
        
        self.key = key
        self.value = value
        self.forward: List[Optional['Node']] = [None] * level



class SkipList:
    """
    Skiplist com balanceamento probabilístico que deve tender a oferecer
    as seguintes operações com as complexidades médias a seguir:
        - Pesquisa O(log n)
        - Inserção O(log n)
        - Deleção O(log n)
    """

    def __init__(self, max_level: int = 4, p: float = 0.5):
        """
        Vai inicializar a skiplist.

        Args:
            max_level (int): O número máximo de levels da estrutura (default 4)
            p (int): O fator aleatório que promove um nível (default 0.5)
        """
        
        self.max_level = max_level
        self.p = p
        self.level = 0 # maior level registrado
        
        self.header = Node(-(sys.maxsize - 1), -(sys.maxsize - 1), self.max_level + 1) # Header negativo

    def _random_level(self) -> int:
        """
        Gera um level aleatório no qual o Node será adicionado.
        """

        level = 0
        while random() < self. p and level < self.max_level:
            level += 1

        return level

    def search(self, key: int) -> Optional[Any]:
        """
        Procura por uma nova chave na skiplist
        
        Args:
            key (int): A chave que está sendo pesquisada.

        Returns:
            O valor associado a chave indicada.
        """
        
        current = self.header

        for i in range(self.level, -1, -1):
            while (current.forward[i] is not None and
                   current.forward[i].key < key):
                current = current.forward[i]

        current = current.forward[0]

        if current is not None and current.key == key:
            return current.value

        return None

    def insert(self, key: int, value: Any) -> None:
        """
        Operação de inserção na estrutura, com o par chave valor, o nível
        da inserção é determinado aleatoriamente.
        Após o processo de criar o objeto para inserção ele vai procurar atribuir 
        no nível adequado e refazer o processo para todos os elementos seguintes.

        Args:
            key (int): Chave que identifica o nó que você quer encontrar
            value (Any): Valor atribuído ao nó que você quer encontrar
        """
        
        update = [None] * (self.max_level + 1)
        current = self.header
        
        for i in range(self.level, -1, -1):
            
            while (current.forward[i] is not None and 
                   current.forward[i].key < key):
                current = current.forward[i]
            update[i] = current
        
        current = current.forward[0]
        
        if current is not None and current.key == key:
            current.value = value
            return
        
        new_level = self._random_level()
        
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level
        
        new_node = Node(key, value, new_level + 1)

        for i in range(new_level):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def delete(self, key: int) -> bool:
        """
        Deleta um elemento da skiplist.

        Args:
            key (int): Chave que identifica o elemento a ser deletado.
        
        Returns:
            Retorna se conseguiu achar/deletar o nó com a chave indicada.
        """

        # Para anotar os Nodes que precisam atualizar
        update = [None] * (self.max_level + 1)
        current = self.header
        
        # Encontra o node para deletar
        for i in range(self.level, -1, -1):
            while (current.forward[i] is not None and 
                   current.forward[i].key < key):
                current = current.forward[i]
            update[i] = current
        
        # Move pro próximo no level 0
        current = current.forward[0]
        
        # Se não achar
        if current is None or current.key != key:
            return False
        
        # Atualiza os ponteiros seguintes
        for i in range(self.level + 1):
            if update[i].forward[i] != current:
                break
            update[i].forward[i] = current.forward[i]

        # Remove os vazios        
        while self.level > 0 and self.header.forward[self.level] is None:
            self.level -= 1
        
        return True


    def display(self) -> None:
        """Display the skiplist structure (for debugging)."""
        print("Skiplist structure:")
        for level in range(self.level, -1, -1):
            print(f"Level {level}: ", end="")
            node = self.header.forward[level]
            while node is not None:
                print(f"({node.key}: {node.value}) ", end="")
                node = node.forward[level]
            print()
    
    def __contains__(self, key: int) -> bool:
        """Check if key exists in skiplist."""
        return self.search(key) is not None
    
    def __len__(self) -> int:
        """Return the number of elements in the skiplist."""
        count = 0
        current = self.header.forward[0]
        while current is not None:
            count += 1
            current = current.forward[0]
        return count
    
    def keys(self) -> List[int]:
        """Return all keys in sorted order."""
        keys = []
        current = self.header.forward[0]
        while current is not None:
            keys.append(current.key)
            current = current.forward[0]
        return keys
    
    def items(self) -> List[tuple]:
        """Return all key-value pairs in sorted order."""
        items = []
        current = self.header.forward[0]
        while current is not None:
            items.append((current.key, current.value))
            current = current.forward[0]
        return items


# Example usage and testing
if __name__ == "__main__":
    # Create skiplist
    sl = SkipList()
    
    # Test insertions
    print("Inserting elements...")
    elements = [(3, "three"), (7, "seven"), (1, "one"), (4, "four"), 
                (2, "two"), (9, "nine"), (5, "five")]
    
    for key, value in elements:
        sl.insert(key, value)
        print(f"Inserted ({key}: {value})")
    
    print(f"\nSkiplist size: {len(sl)}")
    print(f"All keys: {sl.keys()}")
    
    # Test search
    print("\nSearching for elements...")
    for key in [1, 4, 6, 9]:
        result = sl.search(key)
        print(f"Search {key}: {result if result else 'Not found'}")
    
    # Test membership
    print(f"\n5 in skiplist: {5 in sl}")
    print(f"8 in skiplist: {8 in sl}")
    
    # Test deletion
    print("\nDeleting elements...")
    for key in [4, 1, 10]:
        deleted = sl.delete(key)
        print(f"Delete {key}: {'Success' if deleted else 'Not found'}")
    
    print(f"\nFinal keys: {sl.keys()}")
    print(f"Final items: {sl.items()}")
    
    # Display structure
    print()
    sl.display()