import json
import datetime
import redis

# Global cache data structure
class Cache():
    
    def __init__ (self):
        print("Initializing object")
        self.cache = {}
        self.writeLock = False
        self.redis = redis.Redis(host="127.0.0.1", port=6739, db=0)
        self.debug = False
        self.maxKeys = 0
        self.globalExpiry = 0

    def add(self, key):
        if self.debug: print("Refreshing key %s"%(key))

        if len(self.cache) >= self.maxKeys:
            self.lruCleanup()

        try:
            if self.redis.get(key):
                if self.debug: print(" Fetching key from Redis %s"%(key))

                # TODO, what do we do if redis is not available?
                entry = CacheEntry(self.redis.get(key))
                self.cache[key] = entry
                return True
            return False
        except Exception as ex:
            print ('Error:', ex)
            return False

    def lruCleanup(self):
        if self.debug: print("Running LRU")
        lru = ""
        lruTime = datetime.datetime.now()
        cacheKeys = self.cache.keys()
        for key in cacheKeys:
            lastused = self.get(key).lastused
            if (lruTime - lastused).microseconds > 0:
                lru = key
                lruTime = lastused
                if self.debug: print("  Set %s to lru key"%(lru))
        
        self.delete(lru)


    def get(self, key):
        if self.debug: print(" Getting key %s"%(key))
        if key not in self.cache.keys():
            self.add(key)
            if key not in self.cache.keys():
                return False
        else:
            if (datetime.datetime.now() - self.cache[key].created).microseconds >= self.getExpiry() * 1000:
                self.refresh(key)

        return self.cache[key]

    def delete(self, key):
        if self.debug: print(" Deleting key %s"%(key))

        if key in self.cache.keys():
            if self.debug: print(" Deleting key %s"%(key))
            del self.cache[key]
        return True

    def refresh(self, key):
        if self.debug: print(" Refreshing key %s"%(key))
        self.delete(key)
        self.add(key)

    def __repr__(self):
        output = {}
        for key in self.cache.keys():
            output[key] = str(self.cache[key])
        return json.dumps(output)

    def getExpiry(self):
        return self.globalExpiry

    def setRedis(self, host, port, db):
        try:
            self.redis = redis.Redis(host=host, port=port, db=db)
            self.redis.ping()
            if self.debug: print("Redis connected successfully")
        except Exception as ex:
            print ('Error:', ex)
            exit('Failed to connect to Redis server')

    def setExpiry(self, exp):
        self.globalExpiry = exp

    def setDebug(self, debug):
        self.debug=debug

    def setMaxKeys(self, count):
        self.maxKeys = count

class CacheEntry():  
    def __init__ (self, data):
        self.lastused = datetime.datetime.now()
        self.created = datetime.datetime.now()
        self.data = data

    def read(self):
        self.lastused = datetime.datetime.now()
        return self.data

    def __repr__(self):
        return json.dumps({
            'data' : self.data.decode("utf-8"),
            'lastused': str(self.lastused),
            'created': str(self.created)
        })