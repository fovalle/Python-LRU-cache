import cPickle
from lrudal import DAL
from threading import Thread
    
class LRUmap:
    class Node:
        # Node is the container of the cache data, the value from the (key, value) pairs
        # Each node contains a ref to a next node, a ref to a previous node and a ref to its key 
        # in the hashtable (python dictionary) 
        def __init__(self, data=None, parentkey=None):
            self.data = data
            self.next = None
            self.previous = None
            self.parentkey = parentkey
        def __str__(self):
            return str(self.data)
        
    def __init__(self, maxsize=10, overflow=2, checktime=2): 
        #Constructor
        # data -> hashtable with key,value pairs
        # head -> head reference of doubled linked list for LRU cache eviction
        # tail -> tail reference of doubled linked list for LRU cache eviction
        self.data = {}
        self.head = None
        self.tail = None
        self.maxsize = maxsize
        self.overflow = overflow
        self.checktime = checktime
        self.warmUp()
        try:
            Thread(target=self.monitor, args=()).start()
        except Exception, errtxt:
            print errtxt    
    
    def warmUp(self):
        # Get data from DB to populate cache
        dal = DAL()
        for key, value in dal.getKeyValues():
            self.insertInCache(key, cPickle.loads(value))
    
    def get(self, key):
        # get value from cache or from DB and update cache
        if key in self.data:
            node = self.data[key]
            previous = node.previous
            next = node.next
            if previous != None:
                previous.next = next
            else:
                self.head = next    
            if next != None:
                next.previous = previous
            else:
                self.tail = previous    
            node.next = None
            node.previous = None
            self.appendNode(node)
            return node.data
        else:
            dal = DAL()
            value = dal.getValue(key)
            if value != None:
                self.insertInCache(key, value)
                return value
            else:    
                return "Error: key %s not found" % key  
    
    def put(self, key, value):
        # Put key, value pair in cache and DB
        self.insertInCache(key, value)
        dal = DAL()
        dal.update(key, value)
        
    def insertInCache(self, key, value):
        # Put key, value in cache
        node = self.Node(value, key)
        self.appendNode(node)
        self.data[key] = node
    
    def appendNode(self, node):
        # append node to the end of the list for LRU eviction
        if self.head == None:
            self.head = node
            self.tail = node
        else:      
            self.tail.next = node
            node.previous = self.tail
            self.tail = node
        
    def eviction(self):
        # eviction of elements, dependes on max size and overflow
        size = len(self.data)
        if size >= (self.maxsize + self.overflow):
            while size > self.maxsize:
                node = self.head
                self.head = node.next
                node.next.previous = None
                del self.data[node.parentkey]
                size -= 1
            print "Evicting..."    
            self.printCache()
                    
    def printCache(self):
        # Prints LRU cache
        node = self.head
        print "{",
        while node != None:
            print "(",
            print node.parentkey,
            print ",",
            print node,
            print ")",
            node = node.next
        print "}"

    def monitor(self):
        # Monitor size of cache and starts eviction if necessary
        import time
        while True:
            print "Monitoring:"
            self.printCache()
            print "Size: ", len(self.data), " Max+Overflow: ", (self.maxsize + self.overflow) 
            self.eviction()
                
            time.sleep(self.checktime)    