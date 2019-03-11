#!/bin/sh
apk add curl > /dev/null 2>&1

if [ "`curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8888/get/testkey-1`" == "200" ]; then
    echo "Passed http test for success"
else
    echo "Existing key test failed"
fi

if [ "`curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8888/get/nosuchdata`" == "500" ]; then
    echo "Passed http test for missing"
else
    echo "Missing key test failed"
fi