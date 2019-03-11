# Redis HTTP Proxy

## Description

This project acts as a cache in front of a REDIS server and enables a get only HTTP endpoint. It is limited by the maximum keys it will store and will cache only for a specific amount of time

## Architecture

This is developed using Python Tornado to handle the frontend web requests.

The caching library creates 2 objects and uses object methods for all interactions. The Cache object is mostly a wrapper around a cache dictionary which stores key:value pairs, but also adds a dateaccessed and created entry to assist with expiration and LRU.

Algorithmic complexity for the LRU is linear with the number of entries in the cache. For every time it runs out of space in the cache it walks the entire cache to find out the oldest entry and removes it. 

## Usage

The application requires the following environtment variables to be set to operate:

 * REDISHOST (defaults to 127.0.0.1)
 * REDISPORT (defaults to 6379)
 * REDISDB (defaults to 0)
 * GLOBALEXPIRY (defaults to 5) - maximum number of seconds that an entry will be considered valid in the cache
 * MAXKEYS (defaults to 5) - maximum number of keys that the proxy will store
 * HTTPPORT (defaults to 8888)
 * DEBUG (defaults False) - enables verbose debugging mode

### CLI Execution
Set environment variables as you would like, and then run the script with:
 
 `python3 ./proxy.py`

### Docker execution
Startup the container with the appropriate values in -e Environment for your environment and start the docker container:
 
 `docker run -d -p 8888:8888 --network=host redis`
 
 Note, this will use host networking, which will allow localhost access, which may or may not be what you want.

### Makefile exeuction
You can use the makefile to run, however none of the environment variables will be ser properly
 
 `make run`

## Testing

To test, run `make test`, which runs the following steps:

* Starts redis container
* Pre-populates redis container with 2 x the number of max keys defined
* queries the keys from the cache to ensure they come back as expected
* Ensures that an invalid entry returns false via unit tests
* Ensures that LRU functions using unit tests
* Ensures that cached entried are expired properly via unit tests
* Tests HTTP Endpoint


## Time Spent
- proxy.py - main HTTP system - 30 minutes
- caching.py - Caching library - 2 hours
- testing - 2 hours
- other - 1 hour

## Known issues
 * no work has been done to ensure write locking on the objects so there is a possibility of data corruption with many clients
 * While it accepts the connection, it only processes sequentially. 
 * Testing could be more in depth 