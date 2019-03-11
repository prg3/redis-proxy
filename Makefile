build:
	docker build -t redis-proxy .

test: clean build
	docker run --network=host -d --name redis redis
	docker run --network=host redis-proxy python3 /app/test.py
	docker run --network=host -d  --name redisproxy redis-proxy
	docker run --network=host -v `pwd`:/app alpine:3.8 sh /app/test.sh
	docker stop redis redisproxy
	docker rm redis redisproxy

clean:
	docker kill redis redisproxy || true
	docker rm -f redis redisproxy || true
	docker rmi -f redis-proxy

run:
	docker run -d -p 8888:8888 --network=host redis