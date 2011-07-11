import MySQLdb, cPickle

class DAL:
    # Data Abstraction Layer for LRU cache, assumes a mysql DB
    # You need to create a db, user and passwd  
    def __init__(self, db={"name":"cache_example", "user":"lru", "passwd":"lrupass"}):
        self.db = db
    
    def _connection(self):
        return MySQLdb.connect(db=self.db["name"], user=self.db["user"], passwd=self.db["passwd"])
    
    def startDB(self, data):
        # Auxiliary function to insert initial values in DB from dictionary "data"
        connection = self._connection()
        cursor = connection.cursor()
        sql = "INSERT INTO keyvalue VALUES(%s, %s)"
        for key in data:
            cursor.execute(sql, (key, MySQLdb.escape_string(cPickle.dumps(data[key],2))) )
        connection.close()
    
    def getKeyValues(self):
        # Get all key,value pairs from DB
        connection = self._connection()
        cursor = connection.cursor()
        sql = "SELECT mykey, myvalue FROM keyvalue"
        cursor.execute(sql)
        connection.close()
        result = cursor.fetchone()
        while result != None:
            yield result
            result = cursor.fetchone()
    
    def getValue(self,key):
        # Return Value from DB, using a Key
        connection = self._connection()
        cursor = connection.cursor()
        sql = "SELECT myvalue FROM keyvalue where mykey = '" +key+ "'"
        cursor.execute(sql)
        connection.close()
        res = cursor.fetchall()
        if len(res) == 0:
            return None
        value = cPickle.loads(res[0][0])
        return value
    
    def update(self, key, value):
        # Updates DB with key,value pair
        connection = self._connection()
        cursor = connection.cursor()
        sql = "REPLACE INTO keyvalue VALUES(%s, %s)"
        cursor.execute(sql, (key, MySQLdb.escape_string(cPickle.dumps(value,2))) )
        connection.close()
        
