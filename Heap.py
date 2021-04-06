class MaxHeap:
    def __init__(self,maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.Heap = [0] * self.maxsize
        self.Heap_Name = [''] * self.maxsize
        
    def parent(self, pos):

        if pos == 0:
            return pos

        return (pos - 1) // 2

    def leftChild(self, pos):

        return 2 * pos + 1

    def rightChild(self, pos):

        return 2 * pos + 2

    def isLeaf(self, pos):

        if pos > ((self.size // 2) - 1) and pos <= self.size:
            return True
        return False

    def insert(self, element,value):

        if self.size >= self.maxsize:
            return
        self.Heap[self.size] = element
        self.Heap_Name[self.size] = value
        current = self.size
    
        while (self.Heap[current] > self.Heap[self.parent(current)]):
                self.Heap[current],self.Heap[self.parent(current)]=(self.Heap[self.parent(current)],self.Heap[current])
                self.Heap_Name[current],self.Heap_Name[self.parent(current)]=(self.Heap_Name[self.parent(current)],self.Heap_Name[current])
                #self.swap(current, self.parent(current))
                current = self.parent(current)   
        
        self.size += 1

    def extractMax(self):
        popped = self.Heap[0]
        popped2 = self.Heap_Name[0]
        self.Heap[0] = self.Heap[self.size-1]
        self.Heap_Name[0] = self.Heap_Name[self.size-1]
        self.Heap[self.size-1]=0
        self.Heap_Name[self.size-1]=0
        self.size -= 1

        pos=0
        while not(self.isLeaf(pos)):
            if (self.Heap[pos] < self.Heap[self.leftChild(pos)] or self.Heap[pos] < self.Heap[self.rightChild(pos)]):

                if (self.Heap[self.leftChild(pos)] >= self.Heap[self.rightChild(pos)]):
                    #self.swap(pos, self.leftChild(pos))
                    self.Heap[pos], self.Heap[self.leftChild(pos)] = (self.Heap[self.leftChild(pos)], self.Heap[pos])
                    self.Heap_Name[pos], self.Heap_Name[self.leftChild(pos)] = (self.Heap_Name[self.leftChild(pos)], self.Heap_Name[pos])
                    pos = self.leftChild(pos)

                else:
                    #self.swap(pos, self.rightChild(pos))
                    self.Heap[pos], self.Heap[self.rightChild(pos)] = (self.Heap[self.rightChild(pos)], self.Heap[pos])
                    self.Heap_Name[pos], self.Heap_Name[self.rightChild(pos)] = (self.Heap_Name[self.rightChild(pos)], self.Heap_Name[pos])
                    pos = self.rightChild(pos)
            else:
                break

        return popped
