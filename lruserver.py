from SimpleXMLRPCServer import SimpleXMLRPCServer
from lru import LRUmap

class LRU:
    def __init__(self):
        #inits LRU cache, Server and Data Structure
        self.lru = LRUmap(maxsize=11, overflow=3, checktime=2)
    
    def get(self, key):
        #Exposed RPC to get data with a Key
        return self.lru.get(key)
    
    def put(self, key, value):
        #Exposed RPC to put data with a Key, Value pair
        self.lru.put(key, value)

class LRUserver:
    def __init__(self, port=8080):
        # Server will be in localhost port 8080
        self.port = port
        self.server = SimpleXMLRPCServer(("localhost", self.port), allow_none=True)
        self.server.register_instance(LRU())
        self.server.serve_forever()

if __name__=="__main__":
    LRUserver()