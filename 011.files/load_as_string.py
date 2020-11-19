import json
import redis
import time

if __name__ == '__main__':

    r = redis.StrictRedis(host='localhost', port=6379, db=4)

    print('Load json as true-string.')
    with open('data.json', encoding='cp1251') as input_file:
        test_data = json.load(input_file)
        count = len(test_data)
        start = time.time()
        for data in test_data:
            r.set('data', str(data).lower())
        end = time.time()
        print('\t', 'Were load:',  count, 'units')
        print('\t', 'Time left:',  end-start, 'ms')
