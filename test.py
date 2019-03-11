import unittest
import os
import redis
import time

from caching import Cache

redisHost = os.getenv("REDISHOST", "127.0.0.1")
redisPort = os.getenv("REDISPORT", 6379)
redisDB = os.getenv("REDISDB", 0)
maxKeys = 5
expiryTime = 2

class TestRedisProxy(unittest.TestCase):
    cache = Cache()
    cache.setDebug(False)
    cache.setRedis(redisHost, redisPort, redisDB)
    cache.setExpiry(expiryTime)
    cache.setMaxKeys(maxKeys)

    def test_cache(self):
        i=0
        while i <= 2 * maxKeys:
            data = self.cache.get("testkey-%s"%(i)).data
            self.assertEqual(int(data), i)
            i = i + 1        
            
    def test_missing(self):
        self.assertEqual(self.cache.get("nosuchkey"), False)
        
    def test_lru(self):
        data = self.cache.get("lrutest")
        lruDate = data.created
        i = 0
        while i <= 2 * maxKeys:
            self.cache.get("testkey-%s"%(i))
            i = i + 1
            time.sleep(1)
        data = self.cache.get("lrutest")
        self.assertNotEqual(data.created, lruDate)
        
    def test_expiry(self):
        entry = self.cache.get("testkey-%s"%(1))
        time.sleep(expiryTime+1)
        newentry = self.cache.get("testkey-%s"%(1))
        self.assertNotEqual(entry.created, newentry.created)
        

def preloadRedis():
    print ("Preloading redis with %i values"%(2 * maxKeys))
    conn = redis.Redis(host=redisHost, port=redisPort, db=redisDB)
    try:
        conn.ping
    except Exception as ex:
        print ('Error:', ex)
        exit('Failed to connect to Redis server')
    
    i = 0
    while i <= 2 * maxKeys:
        conn.set("testkey-%s"%(i), i)
        i = i + 1
    conn.set("lrutest", "lrupayload")

if __name__ == '__main__':
    preloadRedis()
    unittest.main()