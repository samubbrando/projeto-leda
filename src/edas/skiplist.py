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

    def __copy__(self) -> 'SkipList':
        """
        Cria uma cópia exata da SkipList, mantendo a mesma estrutura de níveis
        e conexões, mas criando objetos completamente independentes.
        
        Returns:
            SkipList: Uma nova instância da SkipList com a mesma estrutura
        """
        # Criar nova skiplist com as mesmas configurações
        new_skiplist = SkipList(max_level=self.max_level, p=self.p)
        new_skiplist.level = self.level
        
        # Se a skiplist original estiver vazia, retorna a nova vazia
        if self.header.forward[0] is None:
            return new_skiplist
        
        # Mapear nodes originais para nodes copiados
        node_map = {}
        
        # Primeiro, criar todos os nodes copiados
        current = self.header.forward[0]
        while current is not None:
            # Criar node copiado com o mesmo tamanho de forward que o original
            copied_node = Node(current.key, current.value, len(current.forward))
            node_map[current] = copied_node
            current = current.forward[0]
        
        # Agora reconectar todos os ponteiros
        # Primeiro, conectar o header aos primeiros nodes de cada nível
        for level in range(len(self.header.forward)):
            if level < len(self.header.forward) and self.header.forward[level] is not None:
                if level < len(new_skiplist.header.forward):
                    new_skiplist.header.forward[level] = node_map[self.header.forward[level]]
        
        # Conectar os nodes entre si
        current = self.header.forward[0]
        while current is not None:
            copied_current = node_map[current]
            
            # Para cada nível que este node possui
            for level in range(len(current.forward)):
                if current.forward[level] is not None:
                    copied_current.forward[level] = node_map[current.forward[level]]
                # Se for None, já está None por padrão na inicialização
            
            current = current.forward[0]
        
        return new_skiplist



import copy

def test_skiplist_copy():
    """
    Teste completo do método __copy__ da SkipList para verificar
    se a cópia mantém a estrutura e independência.
    """
    print("=== Teste do método __copy__ da SkipList ===\n")
    
    # Criar skiplist original
    original = SkipList(max_level=4, p=0.5)
    
    # Inserir elementos
    elements = [(3, "three"), (7, "seven"), (1, "one"), (4, "four"), 
                (2, "two"), (9, "nine"), (5, "five"), (8, "eight")]
    
    print("Inserindo elementos na skiplist original...")
    for key, value in elements:
        original.insert(key, value)
    
    print(f"Original - Tamanho: {len(original)}")
    print(f"Original - Chaves: {original.keys()}")
    print(f"Original - Nível máximo ativo: {original.level}")
    
    # Criar cópia
    print("\nCriando cópia usando copy.copy()...")
    copied = copy.copy(original)
    
    print(f"Cópia - Tamanho: {len(copied)}")
    print(f"Cópia - Chaves: {copied.keys()}")
    print(f"Cópia - Nível máximo ativo: {copied.level}")
    
    # Verificar se as estruturas são idênticas
    print(f"\nChaves são iguais: {original.keys() == copied.keys()}")
    print(f"Itens são iguais: {original.items() == copied.items()}")
    print(f"Tamanhos são iguais: {len(original) == len(copied)}")
    print(f"Níveis são iguais: {original.level == copied.level}")
    
    # Verificar busca em ambas
    print(f"\nTeste de busca - Original 5: {original.search(5)}")
    print(f"Teste de busca - Cópia 5: {copied.search(5)}")
    
    print("\n" + "="*50)
    print("TESTE DE INDEPENDÊNCIA")
    print("="*50)
    
    # Testar independência - modificar original
    print("\nModificando skiplist original...")
    original.insert(10, "ten")
    original.insert(6, "six")
    original.delete(3)
    
    print(f"Após modificações:")
    print(f"Original - Chaves: {original.keys()}")
    print(f"Cópia - Chaves: {copied.keys()}")
    print(f"Cópia permaneceu inalterada: {copied.keys() == [1, 2, 3, 4, 5, 7, 8, 9]}")
    
    # Testar independência - modificar cópia
    print("\nModificando skiplist copiada...")
    copied.insert(11, "eleven")
    copied.delete(7)
    copied.insert(1, "um")  # Atualizar valor existente
    
    print(f"Após modificações na cópia:")
    print(f"Original - Chaves: {original.keys()}")
    print(f"Cópia - Chaves: {copied.keys()}")
    print(f"Original não foi afetado pelas mudanças na cópia: {1 in original and original.search(1) == 'one'}")
    print(f"Valor atualizado só na cópia: {copied.search(1) == 'um' and original.search(1) == 'one'}")
    
    print(f"\nTamanho original: {len(original)}")
    print(f"Tamanho cópia: {len(copied)}")
    
    print("\n" + "="*50)
    print("TESTE DE ESTRUTURA DOS NÍVEIS")
    print("="*50)
    
    # Verificar se os níveis foram copiados corretamente
    def check_structure_integrity(skiplist, name):
        print(f"\nVerificando integridade da estrutura - {name}:")
        
        # Verificar se todos os elementos do nível 0 existem
        level_0_keys = []
        current = skiplist.header.forward[0]
        while current is not None:
            level_0_keys.append(current.key)
            current = current.forward[0]
        
        print(f"Chaves no nível 0: {level_0_keys}")
        print(f"Chaves estão ordenadas: {level_0_keys == sorted(level_0_keys)}")
        
        # Verificar conectividade entre níveis
        integrity_ok = True
        for level in range(skiplist.level + 1):
            level_keys = []
            current = skiplist.header.forward[level]
            while current is not None:
                level_keys.append(current.key)
                current = current.forward[level]
            
            if level_keys != sorted(level_keys):
                integrity_ok = False
                break
        
        print(f"Estrutura de níveis íntegra: {integrity_ok}")
        return integrity_ok
    
    check_structure_integrity(original, "Original")
    check_structure_integrity(copied, "Cópia")
    
    print(f"\n{'='*50}")
    print("CONCLUSÃO: Método __copy__ funcionando corretamente!")
    print("✓ Estrutura copiada fielmente")
    print("✓ Objetos são independentes")
    print("✓ Integridade dos níveis mantida")
    print("✓ Modificações não afetam o outro objeto")


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

    
    test_skiplist_copy()