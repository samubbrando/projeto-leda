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
            out += aux.value + ", "
            aux = aux.next
        
        return out[:-2]
    
    def getSize(self):
        return self.size