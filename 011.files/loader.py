import json
import redis
import time

if __name__ == '__main__':

    r = redis.StrictRedis(host='localhost', port=6379, db=3)

    print('string')
    with open('data.json', encoding='cp1251') as input_file:
        test_data = json.load(input_file)
        start = time.time()
        for data in test_data:
            # data_file.write(data.get("RouteNumber")+'\n')
            # print(data)
            r.set('router_number', data.get("RouteNumber"))
        end = time.time()
        print('STRING:',  end-start, 'ms')

    print('https://redis.io/commands/hset')
    with open('data.json', encoding='cp1251') as input_file:
        test_data = json.load(input_file)
        start = time.time()
        for data in test_data:
            try:
                r.hset('route', 'router_number', data.get("RouteNumber"))
            except redis.exceptions.ResponseError as e:
                print(data.get("RouteNumber"))
        end = time.time()
        print('HSET:', end-start, 'ms')

    # TODO: https://pythontic.com/database/redis/sorted%20set%20-%20add%20and%20remove%20elements
    print('https://redis.io/commands/zadd')
    with open('data.json', encoding='cp1251') as input_file:
        test_data = json.load(input_file)
        start = time.time()
        for data in test_data:
            id = data.get("ID")

            key = data.get("system_object_id")
            score = data.get("system_object_id")
            try:
                r.zadd('route', {key: score}, xx=False )
            except redis.exceptions.ResponseError as e:
                # print(data.get("ID"))
                # print(data.get("RouteNumber"))
                pass

        end = time.time()
        print('ZADD:', end-start, 'ms')

    print('https://redis.io/commands/lpush')
    with open('data.json', encoding='cp1251') as input_file:
        test_data = json.load(input_file)
        start = time.time()
        for data in test_data:
            # print(data.get("RouteNumber"))
            try:
                # r.lpush('route', data.get("RouteNumber"))
                r.rpush('RouteNumber', data.get("RouteNumber")  ,0)
            except redis.exceptions.ResponseError as e:
                print('ResponseError ' + data.get("RouteNumber"))

        end = time.time()
        print('LPUSH:', end-start, 'ms')