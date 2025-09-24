class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def isEmpty(self):
        return self.size == 0

    def addFirst(self, value):
        new_node = Node(value)

        if(self.isEmpty()):
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        self.size += 1
    
    def addLast(self, value):
        new_node = Node(value)

        if(self.isEmpty()):
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        
        self.size += 1

    def add(self, index, value):
        if(index < 0 or index > self.size):
            raise IndexError("Invalid index!")
        
        new_node = Node(value)

        if(index == 0):
            return self.addFirst(value)
        elif(index == self.size):
            return self.addLast(value)
        else:
            aux = self.head

            for _ in range(index-1):
                aux = aux.next
            
            new_node.next = aux.next
            new_node.prev = aux
            aux.next.prev = new_node
            aux.next = new_node
        
            self.size += 1

    def getFirst(self):
        if(self.isEmpty()):
            raise ReferenceError("this structure is empty!")
        
        return self.head.value
    
    def getLast(self):
        if(self.isEmpty()):
            raise ReferenceError("this structure is empty!")
        
        return self.tail.value
    
    def get(self, index):
        if(index < 0 or index >= self.size):
            raise IndexError("Invalid index!")
        
        aux = self.head

        for _ in range(index):
            aux = aux.next
        
        return aux.value
    
    def getByValue(self, value):
        if self.isEmpty():
            return -1
        
        aux = self.head
        index = 0
        
        while aux is not None:
            if aux.value == value:
                return index
            aux = aux.next
            index += 1
        
        return -1
    
    def removeFirst(self):
        if(self.isEmpty()):
            raise ReferenceError("this structure is empty!")
        
        v = self.head.value

        if(self.head.next == None):
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        
        self.size -= 1
        return v
    
    def removeLast(self):
        if(self.isEmpty()):
            raise ReferenceError("this structure is empty!")
        
        v = self.tail.value

        if(self.head.next == None):
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        
        self.size -= 1
        return v

    def remove(self, index):
        if(index < 0 or index >= self.size):
            raise IndexError("Invalid index!")

        if index == 0:
            return self.removeFirst()
        elif index == self.size - 1:
            return self.removeLast()
        else:
            aux = self.head

        for _ in range(index):
            aux = aux.next
        
        aux.prev.next = aux.next
        aux.next.prev = aux.prev

        self.size -= 1

        return aux.value
    
    def removeByValue(self, value):
        if self.isEmpty():
            return False
        
        aux = self.head
        index = 0
        
        while aux is not None:
            if aux.value == value:
                self.remove(index)
                return True
            aux = aux.next
            index += 1
        
        return False
    
    def toString(self):
        if(self.isEmpty()):
            return ""
        
        aux = self.head

        out = ""

        while(aux != None):
            out += str(aux.value) + ", "
            aux = aux.next
        
        return out[:-2]
    
    def getSize(self):
        return self.size
    
    def copy(self):
        """
        Cria uma cópia independente da lista ligada.
        Retorna uma nova instância de LinkedList com os mesmos valores.
        """
        new_list = LinkedList()
        
        if self.isEmpty():
            return new_list
        
        aux = self.head
        while aux is not None:
            new_list.addLast(aux.value)
            aux = aux.next
        
        return new_list

    
if __name__ == "__main__":
    print("=== Testando LinkedList com método copy ===\n")
    
    # Teste 1: Cópia de lista vazia
    print("Teste 1: Cópia de lista vazia")
    lista_vazia = LinkedList()
    copia_vazia = lista_vazia.copy()
    print(f"Lista original vazia: {lista_vazia.isEmpty()}")
    print(f"Cópia vazia: {copia_vazia.isEmpty()}")
    print(f"Tamanhos iguais: {lista_vazia.getSize() == copia_vazia.getSize()}")
    print()
    
    # Teste 2: Cópia de lista com um elemento
    print("Teste 2: Cópia de lista com um elemento")
    lista_um = LinkedList()
    lista_um.addFirst("único")
    copia_um = lista_um.copy()
    print(f"Lista original: {lista_um.toString()}")
    print(f"Cópia: {copia_um.toString()}")
    print(f"Conteúdo igual: {lista_um.toString() == copia_um.toString()}")
    print(f"Objetos diferentes: {lista_um is not copia_um}")
    print()
    
    # Teste 3: Cópia de lista com múltiplos elementos
    print("Teste 3: Cópia de lista com múltiplos elementos")
    lista_multi = LinkedList()
    elementos = ["A", "B", "C", "D", "E"]
    for elem in elementos:
        lista_multi.addLast(elem)
    
    copia_multi = lista_multi.copy()
    print(f"Lista original: {lista_multi.toString()}")
    print(f"Cópia: {copia_multi.toString()}")
    print(f"Tamanhos iguais: {lista_multi.getSize() == copia_multi.getSize()}")
    print(f"Conteúdo igual: {lista_multi.toString() == copia_multi.toString()}")
    print()
    
    # Teste 4: Independência das estruturas (modificação não afeta a outra)
    print("Teste 4: Teste de independência")
    lista_original = LinkedList()
    for i in range(1, 6):
        lista_original.addLast(i)
    
    copia_independente = lista_original.copy()
    
    print(f"Antes das modificações:")
    print(f"Original: {lista_original.toString()}")
    print(f"Cópia: {copia_independente.toString()}")
    
    # Modificar lista original
    lista_original.addLast(6)
    lista_original.removeFirst()
    
    # Modificar cópia
    copia_independente.addFirst(0)
    copia_independente.removeLast()
    
    print(f"Após modificações:")
    print(f"Original: {lista_original.toString()}")
    print(f"Cópia: {copia_independente.toString()}")
    print(f"São diferentes: {lista_original.toString() != copia_independente.toString()}")
    print()
    
    # Teste 5: Verificação de integridade da cópia
    print("Teste 5: Verificação de integridade da cópia")
    lista_teste = LinkedList()
    valores = [10, 20, 30, 40, 50]
    for v in valores:
        lista_teste.addLast(v)
    
    copia_teste = lista_teste.copy()
    
    # Verificar se todos os elementos foram copiados corretamente
    print(f"Verificando elementos individuais:")
    for i in range(copia_teste.getSize()):
        original_val = lista_teste.get(i)
        copia_val = copia_teste.get(i)
        print(f"Posição {i}: Original={original_val}, Cópia={copia_val}, Igual={original_val == copia_val}")
    
    print(f"Head da original: {lista_teste.getFirst()}")
    print(f"Head da cópia: {copia_teste.getFirst()}")
    print(f"Tail da original: {lista_teste.getLast()}")
    print(f"Tail da cópia: {copia_teste.getLast()}")
    print()
    
    # Teste 6: Performance com lista maior
    print("Teste 6: Teste com lista maior (1000 elementos)")
    lista_grande = LinkedList()
    for i in range(1000):
        lista_grande.addLast(f"elemento_{i}")
    
    copia_grande = lista_grande.copy()
    print(f"Lista grande copiada com sucesso!")
    print(f"Tamanho original: {lista_grande.getSize()}")
    print(f"Tamanho da cópia: {copia_grande.getSize()}")
    print(f"Primeiro elemento igual: {lista_grande.getFirst() == copia_grande.getFirst()}")
    print(f"Último elemento igual: {lista_grande.getLast() == copia_grande.getLast()}")
    
    print("\n=== Todos os testes do método copy concluídos! ===")